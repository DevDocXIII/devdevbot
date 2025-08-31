import os
from os import path
import subprocess

def run_python_file(working_directory, file_path, args=None):
    """
    Execute a Python file from a given working directory with optional arguments.

    Parameters
    ----------
    working_directory : str
        The directory in which the file should be executed.
    file_path : str
        Path to the Python file relative to ``working_directory``.
    args : list[str] | None
        Optional command‑line arguments to pass to the script.

    Returns
    -------
    str
        A formatted string that contains the stdout, stderr and any error
        information according to the specification:
        * stdout is prefixed with ``STDOUT:``
        * stderr is prefixed with ``STDERR:``
        * if the process exits with a non‑zero code, the string
          ``Process exited with code X`` is appended
        * if no output is produced, ``No output produced.`` is returned
        * on any exception a string starting with ``Error: executing Python
          file`` is returned
    """
    if args is None:
        args = []

    # Resolve absolute working directory
    abs_work_dir = path.abspath(working_directory)

    # Resolve the full path to the target file
    full_path = os.path.realpath(os.path.join(abs_work_dir, file_path))

    # ----- 1. Directory containment check  -----
    if os.path.commonpath([abs_work_dir, full_path]) != abs_work_dir:
        return (
            f'Cannot execute "{file_path}" as it is outside the '
            "permitted working directory"
        )

    # ----- 2. File existence check  -----
    if not os.path.exists(full_path):
        return f'File "{file_path}" not found'

    # ----- 3. Ensure a Python file  -----
    if not file_path.endswith(".py"):
        return f'File "{file_path}" is not a Python script'

    # ----- 4. Build the command -----
    cmd = ["python3", full_path] + args

    try:
        result = subprocess.run(
            cmd,
            cwd=abs_work_dir,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,  # we will handle non‑zero exit codes ourselves
        )

        # Format the output
        output_parts = []

        if result.stdout:
            output_parts.append(f"STDOUT:\n{result.stdout.strip()}")
        else:
            output_parts.append("No output produced.")
        if result.stderr:
            output_parts.append(f"STDERR:\n{result.stderr.strip()}")

        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")
        return "\n".join(output_parts)

    except subprocess.TimeoutExpired as exc:
        return f"Error: executing Python file - timed out after {exc.timeout}s"

    except Exception as exc:  # Catch any other exception
        return f"Error: executing Python file - {exc}"

