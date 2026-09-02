import os
from config import MAX_CHARS
def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        wd_abs_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(wd_abs_path, file_path))

        if os.path.commonpath([wd_abs_path, target_dir]) != wd_abs_path:
            return f'Error: cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_dir):
            return f'Error: file not found or is not a regular file: "{file_path}"'

        with open(target_dir, "r") as f:
            contents = f.read(MAX_CHARS)
            if f.read(1):
                contents += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return contents

    except Exception as e:
        return f"Error: could not get file content {e}"

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": f"Returns the content (at most {MAX_CHARS}) of a file at a specified directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Directory path to a file relative to the working directory (default is the working directory itself)",
                },
            },
            "required": ["file_path"],
        },
    },
}
