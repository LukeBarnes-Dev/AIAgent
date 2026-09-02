
import os
import argparse
import json
from dotenv import load_dotenv
from openai import OpenAI

from functions.call_function import available_functions
#from prompts import system_prompt

def main():
    # remember source .venv/bin/activate
    # run main with uv run main.py
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not set")
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

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
    response = client.chat.completions.create(
        model="openrouter/free",
        messages = messages,
        tools=available_functions,
        temperature=0,
    )

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        if response.usage:
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
        else:
            raise RuntimeError("Response usage property not found")
    message = response.choices[0].message

    if message.tool_calls:
        for call in message.tool_calls:
            function_args = json.loads(call.function.arguments or "{}")
            print(f"Calling function: {call.function.name}({function_args})")
    else:
        print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
