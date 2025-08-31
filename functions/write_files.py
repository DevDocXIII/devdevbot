# functions/write_files.py
"""
Utility for writing a string to a file within a sandboxed directory.

Writes a string to `file_path` relative to `working_directory`,
ensuring the target cannot escape the sandbox.  Returns a short
SUCCESS/ERROR message with the character count.
"""
import os
from pathlib import Path
from google.genai import types

def write_file(
    file_path: str,                          # <-- no default, comes first
    content: str,
    working_directory: str = os.getcwd()
) -> str:
    """
    Write ``content`` to ``file_path`` relative to ``working_directory``.

    Parameters
    ----------
    working_directory : str
        Base directory that defines the sandbox.
    file_path : str
        Target file path (relative to ``working_directory``).
    content : str
        Data to be written.

    Returns
    -------
    str
        A message starting with ``SUCCESS:`` on success or ``Error:`` on
        failure.  The message includes the number of characters written.
    """
    sandbox = Path(working_directory).resolve()
    full_path = (sandbox / file_path).resolve()

    # Verify the file stays inside the sandbox
    try:
        full_path.relative_to(sandbox)
    except ValueError:
        return (
            f'Error: Cannot write to "{file_path}" as it is outside the '
            'permitted working directory'
        )

    # Ensure the destination directory exists
    parent_dir = full_path.parent
    try:
        parent_dir.mkdir(parents=True, mode=0o777, exist_ok=True)
    except OSError as e:
        return f'Error creating directory "{parent_dir}": {e}'

    # Write the file
    try:
        with full_path.open('w', encoding='utf-8') as fp:
            fp.write(content)
    except OSError as e:
        return f'Error writing file "{full_path}": {e}'
   
    return (
        f'SUCCESS: wrote to "{file_path}" '
        f'({len(content)} characters written)'
    )


# ---- Schema for Gemini ---------------------------------------
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description=(
        "Create or overwrite a file relative to the working directory. "
        "Creates any missing directories automatically."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path of the file to write.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text that will be written to the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)

def main():
    result = write_file("calculator", "lorem.txt",
                       "wait, this isn't lorem ipsum")
    print(result)  
    
if __name__ == "__main__":
    main()
