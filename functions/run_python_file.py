import os
import subprocess


def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        wd_abs_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(wd_abs_path, file_path))

        if os.path.commonpath([wd_abs_path, target_dir]) != wd_abs_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if file_path[len(file_path) - 3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", target_dir]
        if args:
            command.extend(args)
        completed_process = subprocess.run(
            command,
            cwd=wd_abs_path,
            capture_output=True,
            text=True,
            timeout=30,
        )
        output: list[str] = []
        if completed_process.returncode != 0:
            output.append(f"Process exited with code {completed_process.returncode}")
        if not completed_process.stdout and not completed_process.stderr:
            output.append(f"No output produced")
        if completed_process.stdout:
            output.append(f"STDOUT:\n{completed_process.stdout}")
        if completed_process.stderr:
            output.append(f"STDERR:\n{completed_process.stderr}")
        return "\n".join(output)
    except Exception as e:
        return f'Error: could not run python script {e}'

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes the specified Python file within the current working directory and returns its output",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The name of the file to run",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional arguments to be provided to the python script as a list of strings"
                },
            },
            "required": ["file_path"],
        },
    },
}
