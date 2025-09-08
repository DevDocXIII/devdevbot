# main.py
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_function import call_function, available_functions, arg_whitelists
from prompts import SYSTEM_PROMPT
from config import MAX_ITERATIONS, GEMINI_MODEL, LOG_PATH, WORKING_DIRECTORY
os.makedirs(os.path.dirname(LOG_PATH) or ".", exist_ok=True)
from functions.cache import ToolCache
from functions.utils import normalize_args



tool_cache = ToolCache()

CACHEABLE = {"get_files_info", "get_file_content"}
# ----------------------------------------------------------------------
# 1️⃣ Helper utilities
# ----------------------------------------------------------------------
def load_api_key() -> str:
    load_dotenv()
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        print("Error: GEMINI_API_KEY not found in environment.")
        sys.exit(1)
    return key

def print_verbose(msg: str, verbose: bool, *args) -> None:
    if verbose:
        print(msg.format(*args))

# ----------------------------------------------------------------------
# 2️⃣ Main loop
# ----------------------------------------------------------------------
def main() -> None:
    verbose = "--verbose" in sys.argv
    user_args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not user_args:
        print("DevDevBot Code Assistant:")
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "How do I build a calculator app?"\n')
        sys.exit(1)

    api_key = load_api_key()
    client = genai.Client(api_key=api_key)
    
    user_prompt = " ".join(user_args)
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    turn = 0
    while turn < MAX_ITERATIONS:
        turn += 1
        continue_loop = generate_content(client, messages, user_prompt, verbose)
        if not continue_loop:  # no more turns
            break

    print(f"Finished after {turn} turn(s).")

def default_verifier(payload) -> bool:
    if payload.get("kind") == "run":
        art = payload.get("artifacts", {})
        return isinstance(art.get("returncode"), int) and art["returncode"] == 0
    if payload.get("kind") == "test":
        return bool(payload.get("artifacts", {}).get("passed"))
    return False

def _append_assistant_text(parts):
    lines = []
    for p in parts:
        if hasattr(p, "text") and p.text:
            lines.append(p.text)
        # optionally serialize function_call objects
        if hasattr(p, "function_call") and p.function_call:
            fc = p.function_call
            lines.append(f"[FUNCTION_CALL] {fc.name}: {fc.args}")
    if lines:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n\n")

# 3️⃣ Interaction with Gemini
def generate_content(client, messages, user_prompt, verbose) -> bool:
    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=SYSTEM_PROMPT,
            ),
        )
    except Exception as exc:
        print(f"Gemini API error: {exc}")
        return False

    if not response.candidates or not getattr(response.candidates[0], "content", None):
        if verbose:
            print("Empty response")
        return False

    content = response.candidates[0].content
    parts = content.parts or []

    # Append assistant once
    assistant_msg = types.Content(role="assistant", parts=parts)
    messages.append(assistant_msg)
    _append_assistant_text(parts)

    calls = [p.function_call for p in parts if getattr(p, "function_call", None)]
    if calls:
        tool_parts = []
        last_payload = None

        for fc in calls:
            name = fc.name
            supplied = normalize_args(fc.args)
            supplied["working_directory"] = WORKING_DIRECTORY
            filtered = {k: v for k, v in supplied.items() if k in arg_whitelists.get(name, set())}

            # try cache for read/list
            resp_part = None
            payload = None
            if name in CACHEABLE:
                cached_part, cached_payload = tool_cache.get(name, filtered)
                if cached_part:
                    resp_part, payload = cached_part, cached_payload

            if resp_part is None:
                # execute tool
                result_msg = call_function(fc, verbose=verbose)
                resp_part = next((pt for pt in (getattr(result_msg, "parts", None) or [])
                                if getattr(pt, "function_response", None)), None)
                if not resp_part:
                    print("Malformed tool response")
                    return False
                payload = getattr(resp_part.function_response, "response", {}) or {}
                # store in cache if cacheable
                if name in CACHEABLE:
                    tool_cache.set(name, filtered, resp_part, payload)

            tool_parts.append(resp_part)
            last_payload = payload
            if verbose:
                print("TOOL PAYLOAD:", payload)

        # respond with exactly one tool message containing all responses
        messages.append(types.Content(role="tool", parts=tool_parts))

        # termination logic
        if last_payload:
            status = last_payload.get("status")
            kind = last_payload.get("kind")
            if status == "error":
                return True
            if status == "noop" and kind == "write":
                return True
            if default_verifier(last_payload):
                return False
        return True
    # No tool call
    first_text = next((p.text for p in parts if hasattr(p, "text") and p.text), None)
    if first_text:
        print(first_text.strip())
    return False

if __name__ == "__main__":
    main()