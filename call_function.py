from functions.get_files_info import get_files_info, get_files_info
from functions.get_files_content import get_files_content, get_files_content
from functions.write_file import write_file, write_file
from functions.run_python_file import run_python_file, run_python_file



from os import name
def call_function(function_call_part, verbose=False):
    if verbose:
        print(f" - Calling function: {function_call_part.name}({function_call_part.argv})")
    else:
        print(f" - Calling function: {function_call_part.name}")

