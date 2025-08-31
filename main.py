import os
import sys 
from google import genai
from google.genai import types
from dotenv import load_dotenv
from functions.config import SYSTEM_PROMPT

def main():
    load_dotenv()
    verbose = True if "--verbose" in sys.argv else False
    args = [] 
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("DevDevBot Code Assistant:")    
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "How do I build a calculator app?"\n')
        sys.exit(1)
    
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key = api_key)

    user_prompt = " ".join(args)
    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [types.Content(role="user", parts = [types.Part(text=user_prompt)]),]

    generate_content(client, messages, user_prompt=user_prompt, verbose=verbose)

def generate_content(client, messages, user_prompt, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents = messages,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT)
    )
        
    if  verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    print("Response:")
    print(response.text)




if __name__ == "__main__":
    main()