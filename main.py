
import os
import argparse
import json
import sys
from dotenv import load_dotenv
from openai import OpenAI

from functions.call_function import available_functions, call_function
#from prompts import system_prompt

def main():
    # remember source .venv/bin/activate
    # run main with uv run main.py
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not set")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    def generate_content(client: OpenAI, messages: list, verbose: bool) -> str | None:
        response = client.chat.completions.create(
            model="openrouter/free",
            messages = messages,
            tools=available_functions,
            temperature=0,
        )
        if not response.usage:
            raise RuntimeError("API response appears to be malformed")

        if verbose:
            print("Prompt tokens:", response.usage.prompt_tokens)
            print("Response tokens:", response.usage.completion_tokens)


        message = response.choices[0].message
        messages.append(message)

        if message.tool_calls:
            for call in message.tool_calls:
                if call.type != "function":
                    continue
                #function_args = json.loads(call.function.arguments or "{}")
                result_message = call_function(call, verbose)

                if not result_message['content']:
                    raise RuntimeError(f"Tool message content not found: {call.function.name}")
                if verbose:
                    print(f"-> {result_message['content']}")
                messages.append(result_message)
        else:
            return message.content
        return None

    for _ in range(20):
        try:
            final_response = generate_content(client, messages, args.verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                return
        except Exception as e:
            print(f"Error in generate_content: {e}")
    print(f"Maximum iterations ({20}) reached")
    sys.exit(1)

if __name__ == "__main__":
    main()
