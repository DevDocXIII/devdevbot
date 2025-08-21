import os
from os import path

def get_files_info(working_directory, directory="."):
    # 1. Make the sandbox absolute once
    sandbox = os.path.abspath(working_directory)

    # 2. Resolve the target directory relative to the sandbox
    full_path = os.path.abspath(path.join(sandbox, directory))


    #print("SANDBOX   :", sandbox)
    #print("FULL_PATH :", full_path)
    #print("Exists?   :", os.path.exists(full_path))
    #print("Is dir?   :", os.path.isdir(full_path))

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
    entries = []
    for name in os.listdir(full_path):
        entry_path = os.path.join(full_path, name)
        # Optional: only files, skip sub‑dirs
        #if os.path.isfile(entry_path):
        size = os.path.getsize(entry_path)
        entries.append(f'{name} ({size} bytes)')



    # 6. Return a readable string
    if not entries:
        return f'{directory} is empty.'
    return '\n'.join(entries)

def get_file_content(working_directory, file_path):
       # 1. Make the sandbox absolute once
    sandbox = os.path.abspath(working_directory)

    # 2. Resolve the target directory relative to the sandbox
    full_path = os.path.abspath(path.join(sandbox, file_path))

    # 3. Boundary check – everything must be inside the sandbox
    if os.path.commonpath([sandbox, full_path]) != sandbox:
        return (
            f'Error: Cannot list "{file_path}" as it is outside the permitted '
            'working directory'
        )
    f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

# Example call (adjust the path to something that exists on your machine)
#print(get_files_info("./", "./test"))
