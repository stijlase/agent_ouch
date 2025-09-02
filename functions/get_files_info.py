import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    full_path_absolute = os.path.abspath(full_path)
    working_directory_absolute = os.path.abspath(working_directory)

    if not full_path_absolute.startswith(working_directory_absolute):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'    
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'
    
    try:
        dir_list = os.listdir(full_path_absolute)
    except Exception as e:
        return f"Error: {e}"
    
    final_list = []

    for item in dir_list:
        full_item = os.path.join(full_path_absolute, item)
        try:
            size = os.path.getsize(full_item)
            is_dir = os.path.isdir(full_item)
        except Exception as e:
            return f"Error: {e}"
        final_list.append(f"- {item}: file_size={size} bytes, is_dir={is_dir}")

    return "\n".join(final_list)



schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)