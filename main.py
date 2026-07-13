import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI


parser = argparse.ArgumentParser(
    prog="Chatbot",
    description="Uses your prompt and gives you an answer",
)
parser.add_argument("user_prompt", type=str, help="user_prompt => Type something to command line for Chatbot.")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output from Chatbot")
args = parser.parse_args()

model_id = "openrouter/free"
message = [
    {"role": "user", "content": args.user_prompt,}
] # User prompt after input(CL) is stored inside args.user_prompt, defined in the first parser.add_argument

def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key == None:
        raise RuntimeError("No api_key found")
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    response = client.chat.completions.create(
        model=model_id, # https://developers.openai.com/api/reference/python/resources/chat/subresources/completions/methods/create
        messages=message
    )

    if response.usage == None:
        raise RuntimeError("failed API request")
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    print(response.choices[0].message.content)







if __name__ == "__main__":
    main()
