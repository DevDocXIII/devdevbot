__all__ = ["get_files_info", "get_file_content"]

import os
from .config import MAX_CHARS

def get_files_info(
    working_directory: str,
    directory: str = "."
) -> str:
    sandbox = os.path.realpath(working_directory)
    full_path = os.path.realpath(os.path.join(sandbox, directory))
    if os.path.commonpath([sandbox, full_path]) != sandbox:
        return (
            f'Error: Cannot read "{directory}" as it is outside the '
            "permitted working directory"
        )
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'

    files_info = []
    for name in os.listdir(full_path):
        if name.startswith("."):
            continue
        filepath = os.path.join(full_path, name)
        is_dir = os.path.isdir(filepath)
        size = os.path.getsize(filepath)
        files_info.append(
            f"- {name} file_size=({size}) bytes,is_dir={is_dir}"
        )

    if not files_info:
        return f'{directory} is empty.'
    return "\n".join(files_info)

def get_file_content(
    working_directory: str,
    file_path: str
) -> str:
    sandbox = os.path.realpath(working_directory)
    full_path = os.path.realpath(os.path.join(sandbox, file_path))
    if os.path.commonpath([sandbox, full_path]) != sandbox:
        return (
            f'Error: Cannot read "{file_path}" as it is outside the '
            "permitted working directory"
        )
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(full_path,"r") as f:
            file_content_string = f.read(MAX_CHARS)
        if os.path.getsize(full_path) > MAX_CHARS:
            file_content_string += (
                f"[...File '{file_path}' truncated at {MAX_CHARS} characters]"
            )
        return file_content_string
    except Exception as e:
        return f'Error reading file "{file_path}": {e}'

