from functions.run_python_file import schema_run_python_file
from google.genai.types import Part
from functions.get_files_info import schema_get_files_info
import os
import sys
import logging
import warnings
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_files_content import get_files_content, schema_get_files_content
from functions.write_file import write_file, schema_write_file
from functions.run_python_file import run_python_file, schema_run_python_file
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_function import call_function

# region Logging & Warning Configuration
warnings.filterwarnings("ignore")

logging.basicConfig(level=logging.ERROR)

for logger_name in ("google", "google.genai", "httpx", "urllib3"):
    logging.getLogger(logger_name).setLevel(logging.ERROR)

os.environ.setdefault("GRPC_VERBOSITY", "ERROR")
os.environ.setdefault("GLOG_minloglevel", "2")
# endregion

def main ():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(
        api_key=api_key
    )

    system_prompt = (
        """
            You are a helpful AI coding agent.

            When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

            - List files and directories
            - Read the Content of a file
            - Write to a file (create or update)
            - Run a python file with optional arguments

            All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
        """
    )

    if len(sys.argv) < 2:
        return
    prompt = sys.argv[1]

    verbose_flag = False
    if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
        verbose_flag = True

    prompt = sys.argv[1]

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_files_content,
            schema_write_file,
            schema_run_python_file
        ]
    )

    config = types.GenerateContentConfig(
        system_instruction=system_prompt,
        tools=[available_functions]
    )


    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=messages,
        config=config
    )
       
    if response is None or response.usage_metadata is None:
        print("response is malformed")
        return

    if verbose_flag:
         print(f"User prompt: {prompt}")
         print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
         print(f"Prompt tokens: {response.usage_metadata.candidates_token_count}")

    if response.function_calls:
        for function_call_part in response.function_calls:
            result = call_function(function_call_part, verbose_flag)
            print(result)
    else:
        print(response.text)


 
   


main()