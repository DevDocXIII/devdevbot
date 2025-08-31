# main.py
import os
import sys 
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.utils import normalize_args

# def parse_function_args(arg: str | dict | None) -> dict:
#     """
#     Convert Gemini’s function‑call arguments into a Python dict.

#     * If `arg` is already a dict, it's returned unchanged.
#     * If `arg` is a JSON string, it's parsed.
#     * If `arg` is `None` or an empty string, an empty dict is returned.
#     """
#     if isinstance(arg, dict):
#         return arg
#     if not arg:  # covers None and ""
#         return {}
#     try:
#         return json.loads(arg)
#     except json.JSONDecodeError:
#         # If the string is malformed, treat it as no arguments
#         return {}

# ──────────────────────────────────────
#  Custom imports
# ──────────────────────────────────────
from functions.config import SYSTEM_PROMPT
from functions.get_files_info import schema_get_files_info, get_files_info

# ──────────────────────────────────────
#  Gemini function tool
# ──────────────────────────────────────
available_functions = types.Tool(
    function_declarations=[schema_get_files_info]
)

# ──────────────────────────────────────
#  Helper functions
# ──────────────────────────────────────
def load_api_key():
    """Load the Gemini API key from the environment."""
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        print("Error: GEMINI_API_KEY not found in environment.")
        sys.exit(1)
    return key

def print_verbose(msg, verbose, *args):
    """Print a message only when verbose mode is enabled."""
    if verbose:
        print(msg.format(*args))

# ──────────────────────────────────────
#  Main entry point
# ──────────────────────────────────────
def main():
    load_dotenv()

    # --- Parse command‑line arguments ------------------------------------
    verbose = "--verbose" in sys.argv
    # collect non‑flag arguments (everything that does NOT start with "--")
    user_args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not user_args:
        print("DevDevBot Code Assistant:")
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "How do I build a calculator app?"\n')
        sys.exit(1)

    api_key = load_api_key()
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(user_args)
    print_verbose("User prompt: {}", verbose, user_prompt)

    # Construct the initial user message for Gemini
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    generate_content(client, messages, user_prompt, verbose)

# python
def generate_content(client, messages, user_prompt, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=SYSTEM_PROMPT,
        ),
    )

    print_verbose(
        "Prompt tokens: {} | Response tokens: {}",
        verbose,
        response.usage_metadata.prompt_token_count,
        response.usage_metadata.candidates_token_count,
    )

    candidate = response.candidates[0]

    # Look for a function call first
    function_part = None
    for part in candidate.content.parts:
        if getattr(part, "function_call", None):
            function_part = part.function_call
            break

    if function_part:
        args = normalize_args(function_part.args)
        print(f"Calling function: {function_part.name}({args})")

        if function_part.name == "get_files_info":
            result = get_files_info(**args)
            # Print raw-ish so tests can see expected substrings
            if isinstance(result, (dict, list)):
                print("Function result:")
                print(result)
            else:
                print("Function result:")
                print(result)
    else:
        # Only print text when there’s no function call
        print("Response:")
        print(response.text or "")

if __name__ == "__main__":
    main()