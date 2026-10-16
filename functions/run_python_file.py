import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:

    working_dir_abs = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))


    try:
        if not os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_file_path[-3:] == ".py":
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file_path]

        if args:
            command.extend(args)

        result = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30)

        result_str = ""
        
        if result.returncode != 0:
            result_str = result_str + f"Process exited with code {result.returncode}"

        if result.stdout == "" and result.stderr == "":
            result_str = result_str + "No output produced"

        if not result.stdout == "":
            if result_str == "":
                result_str = result_str + '\n' 
            result_str = result_str+ f"STDOUT: {result.stdout}"

        if not result.stderr == "":
            if result_str == "":
                result_str = result_str + '\n' 
            result_str = result_str + f"STDERR: {result.stderr}\n"
    
        return result_str
         


    except Exception as e:
        return f"Error: executing Python file: {e}"



schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a Python file in the specified working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to execute, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Arguments to pass to the Python file",
                }
            },
        },
    },
}
