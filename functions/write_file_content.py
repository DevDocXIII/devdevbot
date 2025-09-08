# functions/write_file_content.py
from pathlib import Path
from google.genai import types

def write_file(working_directory: str, file_path: str, content: str):
    sandbox = Path(working_directory).resolve()
    full_path = (sandbox / file_path).resolve()

    # containment check first
    try:
        full_path.relative_to(sandbox)
    except ValueError:
        return {
            "status": "error",
            "kind": "write",
            "details": f'Cannot write outside working dir: "{file_path}"',
        }

    # idempotence check
    existing = None
    if full_path.exists():
        try:
            existing = full_path.read_text(encoding="utf-8")
        except Exception:
            existing = None

    if existing is not None and existing == content:
        return {"status": "noop", "kind": "write", "details": "already up to date"}

    # backup after validations
    if full_path.exists():
        backup_path = full_path.with_suffix(full_path.suffix + ".bak")
        counter = 1
        while backup_path.exists():
            backup_path = full_path.with_suffix(f"{full_path.suffix}.bak.{counter}")
            counter += 1
        full_path.rename(backup_path)

    parent_dir = full_path.parent
    try:
        parent_dir.mkdir(parents=True, mode=0o777, exist_ok=True)
    except OSError as e:
        return {"status": "error", "kind": "write", "details": f"mkdir failed: {e}"}

    try:
        bytes_written = len(content)
        full_path.write_text(content, encoding="utf-8")
    except OSError as e:
        return {"status": "error", "kind": "write", "details": f"write failed: {e}"}

    return {
        "status": "ok",
        "kind": "write",
        "details": f'wrote "{file_path}"',
        "artifacts": {"filepath": str(full_path), "bytes": bytes_written},
    }

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


