# -*- coding: utf-8 -*-
"""
Module: get_files_info
~~~~~~~~~~~~~~~~~~~~~~
Utility helpers for inspecting a sandboxed file system.

The module exposes two public helpers:

- :func:`get_files_info` – enumerate files under a given directory.
- :func:`get_file_content` – read the first *MAX_CHARS* bytes of a file.

Both helpers perform a sandbox boundary check to ensure that the requested path
stays inside the supplied ``working_directory``.  This is useful when the code
is executed in a controlled environment (e.g., a sandboxed CI job or a
restricted CLI tool).
"""

import os
from .config import MAX_CHARS


def get_files_info(
    working_directory: str,
    directory: str = "."
) -> str:
    """
    Return a human-readable listing of files in ``directory``.

    Parameters
    ----------
    working_directory : str
        Base directory that defines the sandbox.  All relative paths are
        resolved against this value.
    directory : str, optional
        Relative path from ``working_directory`` to list.  Defaults to the
        current directory.

    Returns
    -------
    str
        A string that either contains:

        * An error message if the target is outside the sandbox or is not a
          directory.
        * A list of ``- <name> file_size=(<size>) bytes,is_dir=<bool>``
          entries.
        * ``"<directory> is empty."`` when no non-hidden files are present.

    Notes
    -----
    * Hidden files (names starting with a dot) are ignored.
    * The function performs a commonpath check to prevent directory traversal.
    """
    sandbox = os.path.realpath(working_directory)
    full_path = os.path.realpath(os.path.join(sandbox, directory))
    if not os.path.commonprefix([sandbox, full_path]) == sandbox:
        return f'Error: Cannot read "{directory}" outside the working directory.'
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'

    files_info = []
    for name in os.listdir(full_path):
        filepath = os.path.join(full_path, name)
        is_dir = os.path.isdir(filepath)
        size = os.path.getsize(filepath)
        if name.startswith('.'):
            continue
        files_info.append(
            f"- {name} file_size=({size}) bytes,is_dir={is_dir}"
        )

    if not files_info:
        return f'{directory} is empty.'
    return '\n'.join(files_info)


def get_file_content(
    working_directory: str,
    file_path: str
) -> str:
    """
    Read up to ``MAX_CHARS`` bytes from a file and return its content.

    Parameters
    ----------
    working_directory : str
        Base directory that defines the sandbox.
    file_path : str
        Path to the file (relative to ``working_directory``) to read.

    Returns
    -------
    str
        The file content truncated to ``MAX_CHARS`` characters if the file is
        larger.  If the file is smaller, the full content is returned.
        In error cases the string will start with ``"Error:"``.

    Notes
    -----
    * The function enforces the same sandbox boundary check as :func:`get_files_info`.
    * If the file is larger than ``MAX_CHARS``, the string is appended with
      ``"[...File '<file_path>' truncated at <MAX_CHARS> characters]"``.
    """
    sandbox = os.path.realpath(working_directory)
    full_path = os.path.realpath(os.path.join(sandbox, file_path))
    if not os.path.commonprefix([sandbox, full_path]) == sandbox:
        return f'Error: Cannot read "{file_path}" outside the working directory.'
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(full_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if os.path.getsize(full_path) >= MAX_CHARS:   
                file_content_string += (
                    f"[...File '{file_path}' truncated at {MAX_CHARS} characters]"
                )
            return file_content_string
    except Exception as e:
        return f'Error reading file "{file_path}": {e}'


