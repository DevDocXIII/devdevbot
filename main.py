import os
import sys 
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]


def main():
    print("Hello from devdevbot!")
    if len(sys.argv) > 1:
        contents_string = sys.argv[1]
        print(f"argv={sys.argv[1]}")
    else:
        print("Please provide a prompt.")
        sys.exit(1)

    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=f"{messages}",)
        #contents = "hello")
    
    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)
    print(response.text)


if __name__ == "__main__":
    main()