import os
from google.genai import types


def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    full_path_absolute = os.path.abspath(full_path)
    working_directory_absolute = os.path.abspath(working_directory)

    if not full_path_absolute.startswith(working_directory_absolute):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        full_path_dir = os.path.dirname(full_path_absolute)
        if not os.path.exists(full_path_dir):
            os.makedirs(full_path_dir)
        with open(full_path_absolute, "w") as f:
            f.write(content)
    except Exception as e:
        return f"Error: {e}"
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'



schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to a specified file, constrained to the working directory. Will create the file if the specified file does not exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file that will be written to. If it does not exist, it will be created.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written to the file."
            )
        },
        required=["file_path", "content"],
    ),
)