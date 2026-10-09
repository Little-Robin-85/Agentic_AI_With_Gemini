import subprocess
import os
from google.genai import types


def run_python_file(working_directory: str, file_path: str, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(abs_working_dir):
        return f"Error {file_path} is not in the working directory"
    if not os.path.isfile(abs_file_path):
        return f"Error {file_path} is not a file"
    if not file_path.endswith(".py"):
        return f"Error: '{file_path}' is not a Python file"

    try:
        final_args = ["python3", file_path]
        final_args.extend(args) 
        output = subprocess.run(
            final_args, 
            cwd=abs_working_dir, 
            timeout=30,
            capture_output=True)
        final_string =  f"""
        STDOUT: {output.stdout}
        STERR: {output.stderr}
        """

        if output.stdout == "" and output.stderr == "":
            final_string = "No Output Produced\n"

        if output.returncode != 0:
            final_string += f"Process excited with code {output.returncode}"
        
        return final_string

        print(output)
    except Exception as e:
        return f"Error: executing python file: {e}"



schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes .py python files with python3 interpreter. Accepts addition CLI contents as optional array.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="the file to run, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="An optional array of stings to be used as the CLI args for the python file",
                items=types.Schema(
                    type=types.Type.STRING
                )
            ),
        },
    ),
)