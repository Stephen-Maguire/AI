import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        working_directory_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.abspath(os.path.join(working_directory_abs, file_path))
        common_path = os.path.commonpath([working_directory_abs, file_path_abs])
        if not(common_path == working_directory_abs):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(file_path_abs):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not(file_path_abs.endswith(".py")):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", file_path_abs]
        if not(args == None):
            command.extend(args)
        result = subprocess.run(command, cwd = working_directory_abs, capture_output=True, text= True, timeout=30)
        return_string = ""
        if (result.returncode != 0):
            return_string += f"Process exited with code {result.returncode}\n"
        if (result.stderr == "") and (result.stdout == ""):
            return_string += f"No output produced\n"
        else:
            if len(result.stdout)>0:
                return_string += f"STDOUT: {result.stdout}\n"
            if len(result.stderr)>0:
                return_string += f"STDERR: {result.stderr}\n"
        return return_string
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="This is the file path to a .py file relative to the working directory with possible arguments to run in addition",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="A path for the file to run, relative to the working directory",
            ),
            "args": types.Schema(
                type= types.Type.ARRAY,
                items= types.Schema(
                    type=types.Type.STRING
                ),
                description="Extra arguments to be supplied to run the file"
            )
        },    
    required = ["file_path"]
    ),
)
            
