# functions/write_file_content.py
from pathlib import Path
from google.genai import types

def write_file(
    working_directory: str,
    file_path: str,
    content: str) -> str:
    
    sandbox = Path(working_directory).resolve()
    full_path = (sandbox / file_path).resolve()


    # ----‑backup logic‑----
    if full_path.exists():
        backup_path = full_path.with_suffix(full_path.suffix + ".bak")
        # make sure we don’t overwrite an existing backup
        counter = 1
        while backup_path.exists():
            backup_path = full_path.with_suffix(
                f"{full_path.suffix}.bak.{counter}"
            )
            counter += 1
        full_path.rename(backup_path)
        print(f"Backup created: {backup_path}")

    try:
        full_path.relative_to(sandbox)
    except ValueError:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    parent_dir = full_path.parent
    try:
        parent_dir.mkdir(parents=True, mode=0o777, exist_ok=True)
    except OSError as e:
        return f'Error creating directory "{parent_dir}": {e}'

    try:
        with full_path.open("w", encoding="utf-8") as fp:
            fp.write(content)
    except OSError as e:
        return f'Error writing file "{full_path}": {e}'

    return f'SUCCESS: wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file within the working directory. Creates the file if it doesn't exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text that will be written to the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)


