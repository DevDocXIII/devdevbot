import os
from os import path
from os.path import abspath

def get_files_info(working_directory, directory="."):
    # 1. Make the sandbox absolute once
    sandbox = os.path.abspath(working_directory)

    # 2. Resolve the target directory relative to the sandbox
    full_path = os.path.abspath(path.join(sandbox, directory))

    # 3. Boundary check – everything must be inside the sandbox
    if os.path.commonpath([sandbox, full_path]) != sandbox:
        return (
            f'Error: Cannot list "{directory}" as it is outside the permitted '
            'working directory'
        )

    # 4. Ensure the target really is a directory
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'

    # 5. Gather file names & sizes
    files_info = []
    for name in os.listdir(full_path):
        filepath = os.path.join(full_path, name)
        is_dir =  os.path.isdir(filepath)
        size = os.path.getsize(filepath)
        files_info.append(f"- {name} file_size=({size}) bytes,is_dir={is_dir}")

    # 6. Return a readable string
    if not files_info:
        return f'{directory} is empty.'
    return '\n'.join(files_info)

def get_file_content(working_directory, file_path):
       # 1. Make the sandbox absolute once
    sandbox = os.path.abspath(working_directory)
    print(f"sandbox = {sandbox} ")

    # 2. Resolve the target directory relative to the sandbox
    full_path = os.path.abspath(path.join(sandbox, file_path))
    print(f"full_path = {full_path}")

    # 3. Boundary check – everything must be inside the sandbox
    if os.path.commonpath([sandbox, full_path]) != sandbox:
        return (
            f'Error: Cannot list "{file_path}" as it is outside the permitted '
            'working directory'
        )
    f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    # Example call (adjust the path to something that exists on your machine)

def main():
    print(get_files_info("../", "./"))
    print("Result for file:")
    print(f"working {abspath('.')})")
    print(get_file_content(".", './get_files_info.py'))

if __name__=='__main__':
    main()
