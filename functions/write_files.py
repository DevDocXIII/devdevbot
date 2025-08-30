# functions/write_files.py
"""
Utility for writing a string to a file within a sandboxed directory.

The helper guarantees that the write target never escapes the supplied
``working_directory``.  It creates parent directories on demand and
returns a descriptive success or error message.

Usage
-----
>>> write_file("/tmp/sandbox", "sub/hello.txt", "world")
'SUCCESS: wrote to "sub/hello.txt" (5 characters written)'

If the target is outside the sandbox, the function returns an error string.
"""

import os
from pathlib import Path
from typing import Tuple

def write_file(
    working_directory: str, file_path: str, content: str
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

    Notes
    -----
    * The function automatically creates missing parent directories.
    * All paths are resolved with :class:`pathlib.Path` to avoid issues
      with ``..`` traversal.
    * No exceptions are raised – the caller should inspect the return
      string for errors.
    """
    sandbox = Path(working_directory).resolve()
    full_path = (sandbox / file_path).resolve()

    # Sandbox boundary check
    try:
        full_path.relative_to(sandbox)
    except ValueError:
        return (
            f'Error: Cannot write to "{file_path}" as it is outside the '
            'permitted working directory'
        )

    # Ensure parent directory exists
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

def add_two_number(a, b):
    return a + b
def subtract_number(a, b):
    return a - b
def square_number(a):
    return a ** 2

def main():
    result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")  
def add_two_numbers_and_divide(a, b, c):
    return (a + b) / c
