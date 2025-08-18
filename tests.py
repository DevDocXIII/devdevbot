# tests.py
# -------------  project_root/tests.py -------------
import os
from pathlib import Path

# Import the function we just implemented
from functions.get_files_info import get_files_info


def _print_entries(title: str, entries: str, working_dir: str):
    """
    Pretty‑print the list of entries returned by get_files_info.

    Parameters
    ----------
    title : str
        Header line that will be printed before the list.
    entries : str
        The raw string returned by get_files_info
        (one entry per line in the form:  name (size bytes)).
    working_dir : str
        The absolute path of the sandbox so we can check
        whether each entry is a directory.
    """
    print(title)
    for line in entries.splitlines():
        if not line.strip():
            continue
        # Expected format:  "name (size bytes)"
        name_part, size_part = line.split(" (")
        name = name_part.strip()
        size = int(size_part.split()[0])   # extract the numeric size
        is_dir = os.path.isdir(os.path.join(working_dir, name))
        print(f" - {name}: file_size={size} bytes, is_dir={is_dir}")


def _print_error(title: str, error_msg: str):
    """
    Print the error line with the required indentation.
    """
    print(title)
    print(f"    {error_msg}")          # 4 leading spaces


def main():
    # Base directory relative to the project root
    sandbox = os.path.abspath("calculator")

    # 1. Current directory ('.')
    out1 = get_files_info("calculator", ".")
    if out1.startswith("Error:l"):
        _print_error("Result for current directory:", out1)
    else:
        _print_entries("Result for current directory:", out1, sandbox)

    # 2. pkg directory
    out2 = get_files_info("calculator", "pkg")
    if out2.startswith("Error:"):
        _print_error("Result for 'pkg' directory:", out2)
    else:
        _print_entries("Result for 'pkg' directory:", out2, sandbox)

    # 3. /bin – should trigger an error
    out3 = get_files_info("calculator", "/bin")
    if out3.startswith("Error:"):
        _print_error("Result for '/bin' directory:", out3)
    else:
        _print_entries("Result for '/bin' directory:", out3, sandbox)

    # 4. ../ – also an error
    out4 = get_files_info("calculator", "../")
    if out4.startswith("Error:"):
        _print_error("Result for '../' directory:", out4)
    else:
        _print_entries("Result for '../' directory:", out4, sandbox)


if __name__ == "__main__":
    main()
