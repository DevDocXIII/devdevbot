# tests.py
# ------------------------------------------------------------------
#  Test cases for the `run_python_file` helper
#  ---------------------------------------------------------------

# Imports that were already present in the original file
from unittest import result
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python import run_python_file

def run_tests():
    # # Should print the calculator's usage instructions
    # result = run_python_file("calculator", file_path="main.py")
    # print(result)

    # # Should run the calculator with expression "3 + 5" and produce a rendered result
    # result= run_python_file("calculator", "main.py", args=["3 + 5"])
    # print(result)

    # # Test running this test file itself
    # result = run_python_file("calculator", "tests.py")
    # print(result)

    # # Should error because target file is outside the working directory
    # result = run_python_file("calculator", "../main.py")
    # print(result)

    # # Should error because file does not exist
    # result = run_python_file("calculator", "nonexistent.py")
    # print(result)

    #print get_file_content(".","./"))
    print(get_files_info("./"))



if __name__ == "__main__":
    run_tests()
