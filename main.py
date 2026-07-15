import os
import argparse
import json
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions, call_function


parser = argparse.ArgumentParser(
    prog="Chatbot",
    description="Uses your prompt and gives you an answer",
)
parser.add_argument("user_prompt", type=str, help="user_prompt => Type something to command line for Chatbot.")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output from Chatbot")
args = parser.parse_args()

model_id = "openrouter/free"
messages = [
    {"role": "system", "content": system_prompt,},
    {"role": "user", "content": args.user_prompt,}
] # User prompt after input(CL) is stored inside args.user_prompt, defined in the first parser.add_argument

def main(): # Main function
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key == None:
        raise RuntimeError("No api_key found")
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    #### AI Loop
    for _ in range(20):  # Limit to 20 iteration     
        response = client.chat.completions.create(
            model=model_id, # https://developers.openai.com/api/reference/python/resources/chat/subresources/completions/methods/create
            messages=messages,
            tools=available_functions,
        )
        messages.append(response.choices[0].message) # Making sure that AI 'remembers' his own actions
        if response.choices[0].message.tool_calls:
            for tool_call in response.choices[0].message.tool_calls:               
                messages.append(call_function(tool_call)) # Appending results of every function AI calls for AI to see
        else:
            break # To stop the main loop if there is no tool(function) call meaning that the final result is ready
    ####
    if response.usage == None:
        raise RuntimeError("failed API request")
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
    
    print(f"Final response:\n{response.choices[0].message.content}")
    # r_message = response.choices[0].message
    # if r_message.tool_calls:
    #     for tool_call in r_message.tool_calls:
    #         func_args = json.loads(tool_call.function.arguments or "{}")
    #         print(f" - Calling function: {tool_call.function.name}({func_args})")
            
    #         result_message = call_function(tool_call)
    #         if not result_message["content"]:
    #             raise Exception("No content")
    #         if args.verbose:
    #             print(f"-> {result_message['content']}")
    #         else:
    #             print(f"{result_message['content']}")
    # else:
    #     print(response.choices[0].message.content)







if __name__ == "__main__":
    main()
