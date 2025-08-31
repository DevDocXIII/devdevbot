from google.genai import types
from .config import MAX_CHARS
import os

def get_files_info(
    directory: str = ".",
    working_directory: str = os.getcwd(),  # default to current dir if not given
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

# functions/get_files_info.py
def get_file_content(
    file_path: str,                          # <-- no default, comes first
    working_directory: str = os.getcwd()     # <-- defaulted, comes after
) -> str:
    """Return the content of a file."""
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
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read the contents of the file requested in the specified directory constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
         },
       required=["file_path"],
       )
)
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read the contents of the file requested in the specified directory constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
         },
       required=["file_path"],
       )
)