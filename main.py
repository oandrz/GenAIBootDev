import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file_content import schema_write_file_content, write_file
from functions.run_python_file import schema_run_python_file, run_python_file
WORKING_DIR = "./calculator"


def main(prompt, isVerbose=False):
    # Load environment variables from .env file
    load_dotenv()

    verbose = "--verbose" in sys.argv
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    For your information, working directory is set to the ./calculator directory
    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_write_file_content,
            schema_get_file_content,
            schema_run_python_file,
        ]
    )

    config = types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt
    )

    # Get API key from environment variables
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment variables")
        return
    
    try:
        # Initialize the Gemini client
        client = genai.Client(api_key=api_key)
        
        # Define the prompt
        # prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
        
        # Generate content using the Gemini model
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            config=config,
            contents=messages
        )
        
        # Print the response text
        print("\nResponse:")
        # Check for function calls in the response
        if hasattr(response, "function_calls") and response.function_calls:
            for call in response.function_calls:
                print(f"Function called: {call.name}({call.args})")
                result = call_function(call, isVerbose)
                print(f"-> {result.parts[0].function_response.response}")

            # Fallback to printing the text response
            print("Response text:", response.text)

        # Print token usage
        if hasattr(response, 'usage_metadata') and verbose:
            print(f"User prompt: {prompt}")
            print("\nToken Usage:")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def call_function(function_call_part, verbose=False):
    if verbose:
        print(
            f" - Calling function: {function_call_part.name}({function_call_part.args})"
        )
    else:
        print(f" - Calling function: {function_call_part.name}")
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }
    function_name = function_call_part.name
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    args = dict(function_call_part.args)
    args["working_directory"] = WORKING_DIR
    function_result = function_map[function_name](**args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python greet.py <name>")
        sys.exit(1)
    prompt = sys.argv[1]
    verbose = "--verbose" in sys.argv
    main(prompt, verbose)
