import os
def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        wd_abs_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(wd_abs_path, directory))

        if os.path.commonpath([wd_abs_path, target_dir]) != wd_abs_path:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        #return f'Success: "{directory}" is within the working directory'
        header = f"Result for {target_dir} directory: \n"
        files_info: list[str] = []
        for item in os.listdir(target_dir):
            filepath = os.path.join(target_dir, item)
            is_dir = os.path.isdir(filepath)
            file_size = os.path.getsize(filepath)
            files_info.append(f"-{item}: file_size={file_size} bytes, is_dir={is_dir}")

        return "\n".join(files_info)
    except Exception as e:
        return f"Error listing files: {e}"

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
