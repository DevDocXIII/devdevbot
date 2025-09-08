# functions/get_file_content.py
from google.genai import types
from config import MAX_CHARS
import os
def get_file_content(file_path: str, working_directory: str):
    import os
    base = os.path.realpath(working_directory)
    target = os.path.realpath(os.path.join(base, file_path))
    if os.path.commonpath([base, target]) != base:
        return {"status":"error","kind":"read","details":"outside working dir"}
    if not os.path.isfile(target):
        return {"status":"error","kind":"read","details":f'not a file: "{file_path}"'}
    try:
        with open(target, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        return {"status":"ok","kind":"read","artifacts":{"file_path": file_path, "content": content}}
    except Exception as e:
        return {"status":"error","kind":"read","details": f"read failed: {e}"}

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read the contents of the file requested in the specified directory constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)