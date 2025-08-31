from google.genai import types
from functions.config import MAX_CHARS
import os

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
