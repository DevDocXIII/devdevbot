# functions/run_python.py
import os
import sys
from os import path
import subprocess
from google.genai import types

def run_python_file(
    working_directory,
    file_path, 
    args=None):

    if args is None:
        args = []

    # Resolve absolute working directory
    abs_work_dir = path.abspath(working_directory)

    # Resolve the full path to the target file
    full_path = os.path.realpath(os.path.join(abs_work_dir, file_path))

    # ----- 1. Directory containment check  -----
    if os.path.commonpath([abs_work_dir, full_path]) != abs_work_dir:
        return (
            f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        )

    # ----- 2. File existence check  -----
    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'

    # ----- 3. Ensure a Python file  -----
    if not file_path.endswith(".py"):
        return f'Error: File "{file_path}" is not a Python file.'

    # ----- 4. Build the command -----
    cmd = [sys.executable, full_path] + args

    try:
        result = subprocess.run(
            args=cmd,
            cwd=abs_work_dir,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,  # we will handle non‑zero exit codes ourselves
        )

        output_parts = []

        if result.stdout:
            output_parts.append(f"STDOUT:\n{result.stdout.strip()}")
        if result.stderr:
            output_parts.append(f"STDERR:\n{result.stderr.strip()}")
        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")

        return "\n".join(output_parts) if output_parts else "No output produced."

    except subprocess.TimeoutExpired as e:
        return f"Error: executing Python file - timed out after {e.timeout}s"

    except Exception as e:  # Catch any other exception
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description=(
        "Execute a Python file relative to the working directory and return "
        "its stdout, stderr, and exit code."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the Python file to execute.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of command-line arguments.",
            ),
        },
        required=["file_path"],
    ),
)
