# ------------------------------------------------------------------
#  Test cases for the `run_python_file` helper
#  ---------------------------------------------------------------

# Imports that were already present in the original file
from functions.get_files_info import get_file_content, get_files_info
from functions.write_files import write_file
# The helper being tested
from functions.run_python import run_python_file

def run_tests():
    """
    Execute a suite of manual test cases that exercise `run_python_file`.

    Each call is followed by a short comment explaining the expected behaviour.
    """

    # Should print the calculator's usage instructions
    run_python_file("calculator", "main.py")

    # Should run the calculator with expression "3 + 5" and produce a rendered result
    run_python_file("calculator", "main.py", ["3 + 5"])

    # Test running this test file itself
    run_python_file("calculator", "tests.py")

    # Should error because target file is outside the working directory
    run_python_file("calculator", "../main.py")

    # Should error because file does not exist
    run_python_file("calculator", "nonexistent.py")

if __name__ == "__main__":
    run_tests()
