from functions.config import MAX_CHARS
from google.genai import types
import os

def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    full_path_absolute = os.path.abspath(full_path)
    working_directory_absolute = os.path.abspath(working_directory)

    if not full_path_absolute.startswith(working_directory_absolute):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(full_path_absolute) as f:
            file_content_str = f.read(MAX_CHARS)
            if os.path.getsize(full_path_absolute) > MAX_CHARS:
                file_content_str += f'[...File "{file_path}" truncated at 10000 characters]'
    except Exception as e:
        return f"Error: {e}"
    

    return file_content_str



schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=F"Reads and returns up to {MAX_CHARS} characters of the specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to be read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)