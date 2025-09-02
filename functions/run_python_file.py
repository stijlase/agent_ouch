import os, subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)
    full_path_absolute = os.path.abspath(full_path)
    working_directory_absolute = os.path.abspath(working_directory)

    if not full_path_absolute.startswith(working_directory_absolute):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'    
    if not os.path.exists(full_path_absolute):
        return f'Error: File "{file_path}" not found.'    
    if not full_path_absolute.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    run_list = ["python", file_path] + args
    final = []
    
    try: 
        result = subprocess.run(run_list, timeout=30, capture_output=True, cwd=working_directory_absolute)
        if result.stdout:
            out_bin = result.stdout
            final.append(f"STDOUT: {out_bin.decode()}")
        if result.stderr:
            err_bin = result.stderr
            final.append(f"STDERR: {err_bin.decode()}")
        if result.returncode != 0:
            final.append(f"Process exited with code {result.returncode}")
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
    if not final:
        final = "No output produced"
    else:
        final = "\n".join(final)
    
    return final



schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file in the specified directory, and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the Python file to be ran, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)