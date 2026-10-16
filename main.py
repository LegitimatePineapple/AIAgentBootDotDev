import json
import os
import argparse
import sys
from dotenv import load_dotenv, parser
from openai import OpenAI
from config import MAX_ITERS
from prompts import system_prompt
from call_function import available_functions, call_function

def main() -> None:
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is not set in the environment .")

    client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )

    messages =[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": args.user_prompt},
            ]

    for _ in range(MAX_ITERS):
        try:
            final_response = generate_content(client, messages, args.verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                return
        except Exception as e:
            print(f"Error in generate_content: {e}")

    print(f"Maximum iterations ({MAX_ITERS}) reached")
    sys.exit(1)

    return None



def generate_content(client: OpenAI, messages: list, verbose: bool) -> None:
    response = client.chat.completions.create(
            # model="apodex/apodex-1.1-mini:free",
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
        )

    if not response.usage:
        raise RuntimeError("No usage information found in the response.")
    
    if verbose:
        print(f"-> {result_message['content']}")

    message = response.choices[0].message
    messages.append(message)

    if not message.tool_calls:
        return message.content
    
    
    for tool_call in message.tool_calls:
        if tool_call.type != "function":
            continue

        result_message = call_function(tool_call)

        if not result_message.get("content"):
            raise Exception("Empty Content from tool call")
        
        if verbose:
            print(f"-> {result_message['content']}")
        messages.append(result_message)


    return None
        

if __name__ == "__main__":
    main()
