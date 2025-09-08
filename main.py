# main.py
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_function import call_function, available_functions
from prompts import SYSTEM_PROMPT
from config import MAX_ITERATIONS, GEMINI_MODEL, LOG_PATH
os.makedirs(os.path.dirname(LOG_PATH) or ".", exist_ok=True)

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

    #print_verbose("User prompt: {}", verbose, user_prompt)

    # --- Count turns to avoid infinite loops --------------------------------
    turn = 0
    while turn < MAX_ITERATIONS:
        turn += 1
        continue_loop = generate_content(client, messages, user_prompt, verbose)
        if not continue_loop:  # no more turns
            break

    print(f"Finished after {turn} turn(s).")

# ----------------------------------------------------------------------
# 3️⃣ Verifier function
# ----------------------------------------------------------------------
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
# detect only the first function_call
    func_call = next((getattr(p, "function_call", None) for p in parts if getattr(p, "function_call", None)), None)
    # func_call = next((getattr(p, "function_call", None) for p in parts if getattr(p, "function_call", None)), None)

    if func_call:
        function_call_result = call_function(func_call, verbose=verbose)
        parts_out = getattr(function_call_result, "parts", None)
        if not parts_out:
            print("Malformed tool response: no parts")
            return False
        first_part = parts_out[0]
        if not hasattr(first_part, "function_response") or first_part.function_response is None:
            print("Malformed tool response: missing function_response")
            return False

        messages.append(function_call_result)

        payload = getattr(first_part.function_response, "response", {}) or {}
        status = payload.get("status")
        kind = payload.get("kind")

        if verbose:
            print("TOOL PAYLOAD:", payload)

        if status == "error":
            return True
        if status == "noop" and kind == "write":
            return True
        if default_verifier(payload):
            return False
        return True

    # No tool call
    first_text = next((p.text for p in parts if hasattr(p, "text") and p.text), None)
    if first_text:
        print(first_text.strip())
    return False

if __name__ == "__main__":
    main()