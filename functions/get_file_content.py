import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        working_directory_abs = os.path.abspath(working_directory)
        file_path_abs = os.path.abspath(os.path.join(working_directory_abs, file_path))
        common_path = os.path.commonpath([working_directory_abs, file_path_abs])
        if not(common_path == working_directory_abs):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(file_path_abs):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        content = ""
        with open(file_path_abs, "r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return content
    except Exception as e:
        return f"Error: {e}"
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the content of a file in a specified directory relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
            properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose contents are to be returned, relative to the working directory",
            ),
            },
        required = ["file_path"],
    ),
)