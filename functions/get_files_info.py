import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

    try:
        if not os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        # return f'Success: "{directory}" is within the working directory'    
        file_names = os.listdir(target_dir)
        dir_contents = ""            
        for name in file_names:
                
                file_path = os.path.join(target_dir, name)
                file_info = f"{name}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}"
                if dir_contents == "":
                    dir_contents = file_info
                else:
                    dir_contents += f"\n{file_info}"
                
                
        return dir_contents
                 
            
    except Exception as e:
        return f"Error: {e}"


schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}



    