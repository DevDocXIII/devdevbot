import os
from os import path

def get_files_info(working_directory, directory="."): # type: ignore
    
    full_path = path.abspath(path.join(working_directory, directory))
    
    sandbox = os.path.abspath(working_directory)
    
    common = os.path.commonpath([working_directory, full_path])
    
    

    print(f"full_path={full_path}")
    print(f"root_of_project={sandbox}")
    print(f"whats in common:{common}")
    print(f"common:{common == os.path.abspath(working_directory)}")
    
    
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'
    else:
        print('Its a directory')
        # Check if the directory is outside of the sandbox (not safe)

test = get_files_info("/functions","./etc")
#print( is_safe = (common == os.path.abspath(working_directory)))

