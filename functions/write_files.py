# write_files.py in functions folder
import os
from os import path

def write_file(working_directory, file_path, content):

    sandbox = os.path.abspath(working_directory)
    full_path = os.path.abspath(path.join(sandbox, file_path))

    if os.path.commonpath([sandbox, full_path]) != sandbox:
        return (
            f'Error: Cannot write to "{file_path}" as it is outside the permitted '
            'working directory'
        )

    parent_dir = os.path.dirname(full_path)
    if not os.path.isdir(parent_dir):
        try:
            os.makedirs(parent_dir,0o777,True)
        except Exception as e:
             raise Exception(f"Error: {str(e)}")
             #return f'Error: "{file_path}" is not a directory'
    try:
        with open(full_path, 'w') as file:
            file.write(content)
    except Exception as e:
        return f'Error writing file "{full_path}": {e}'
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
   