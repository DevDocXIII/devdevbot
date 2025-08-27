# tests.py
# -------------  project_root/tests.py -------------
# Import the function we just implemented
from functions.get_files_info import get_files_info
def main():
    # 1. Current directory ('.')
    result  = get_files_info("calculator", ".")
    print("\nResult for current directory:")
    print(result)
    # 2. pkg directory
    print("\nResult for 'pkg' directory:")
    result = get_files_info("calculator", "pkg")
    print(result)
    # 3. /bin – should trigger an error
    print("\nResult for '/bin' directory:")
    result = get_files_info("calculator", "/bin")
    print(result)
    # 4. ../ – also an error
    print("\nResult for '../' directory:")
    result  = get_files_info("calculator", "../")
    print(result)


if __name__ == "__main__":
    main()
