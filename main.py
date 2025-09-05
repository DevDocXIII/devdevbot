# main.py
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_function import call_function, available_functions
from prompts import SYSTEM_PROMPT
from config import MAX_ITERATIONS   

def load_api_key():
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        print("Error: GEMINI_API_KEY not found in environment.")
        sys.exit(1)
    return key

def print_verbose(msg, verbose, *args):
    if verbose:
        print(msg.format(*args))

def main():
    load_dotenv()
    verbose = "--verbose" in sys.argv
    user_args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
    if not user_args:
        print("DevDevBot Code Assistant:")
        print('\nUsage: python main.py \"your prompt here\"')
        print('Example: python main.py \"How do I build a calculator app?\"\\n')
        sys.exit(1)
    api_key = load_api_key()
    client = genai.Client(api_key=api_key)
    user_prompt = " ".join(user_args)
    print_verbose("User prompt: {}", verbose, user_prompt)
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]
    # Generate content using the client and messages
    generate_content(client, messages, user_prompt, verbose)

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

    if not response.candidates:
        print(response.text or "")
        return

    func_call = None
    for c in response.candidates or []:
        parts = getattr(getattr(c, "content", None), "parts", None) or []
        for p in parts:
            if getattr(p, "function_call", None):
                func_call = p.function_call
                break
        if func_call:
            break

    function_call_result = None  # ensure bound

    if func_call:
        function_call_result = call_function(func_call, verbose=verbose)

        # validate result presence
        if (
            not function_call_result.parts
            or not hasattr(function_call_result.parts[0], "function_response")
            or function_call_result.parts[0].function_response is None
        ):
            raise RuntimeError("Function call result missing response")

        result_dict = function_call_result.parts[0].function_response.response or {}
        output_text = result_dict.get("result", "") or result_dict.get("error", "")
        
        if output_text:
            print(output_text)
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
    else:
        # No function call: just print the model’s text if any
        if response.text:
            print(response.text)
            print_verbose("Function call result missing response", verbose=verbose)
if __name__ == "__main__":
    main()

