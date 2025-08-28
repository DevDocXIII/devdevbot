# tests.py
# -------------  project_root/tests.py -------------
from functions.get_files_info import get_file_content, get_files_info
from functions.write_files import write_file

# Test cases for get_files_info
def test_get_files_info():
     assert get_files_info(".", "./") == "Error: Cannot read \"./\" as it is outside the permitted working directory"
     assert get_files_info(".", "../") == "Error: Cannot read \"../\" as it is outside the permitted working directory"
def main():
    result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print(result)

    result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print(result)

    result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print(result)
    
if __name__ == "__main__":
    main()
