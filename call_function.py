from asyncio import base_events
from functions.get_files_info import get_files_info, get_files_info
from functions.get_files_content import get_files_content, get_files_content
from functions.write_file import write_file, write_file
from functions.run_python_file import run_python_file, run_python_file
from google.genai import types

working_directory = "calculator"

from os import name
def call_function(function_call_part, verbose=False):
    if verbose:
        print(f" - Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")


    if function_call_part.name == "get_files_info":
        result = get_files_info(working_directory, **function_call_part.args)

    if function_call_part.name == "get_files_content":
        result = get_files_content(working_directory, **function_call_part.args)

    if function_call_part.name == "write_file":
        result = write_file(working_directory, **function_call_part.args)

    if function_call_part.name == "run_python_file":
        result = run_python_file(working_directory, **function_call_part.args)
    
    if result == "":
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": function_call_part.name}
                )
            ],
        )


    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": result}
            )
        ],
    )
