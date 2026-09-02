import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        wd_abs_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(wd_abs_path, file_path))

        if os.path.commonpath([wd_abs_path, target_dir]) != wd_abs_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_dir):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        os.makedirs(os.path.dirname(target_dir), exist_ok=True)
        with open(target_dir, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: could not write to file {e}'

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes content into a file at a given file path with content provided as an argument.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Directory path to a file relative to the working directory (default is the working directory itself)",
                "content": {
                    "type": "string",
                    "description": "Content to be written into the specified file"
                }
                },
            "required": ["file_path", "content"]

            },

        },
    },
}
