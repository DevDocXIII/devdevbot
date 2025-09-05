# funtions/get_files_info.py
from google.genai import types
import os
from typing import Any, Dict, List, Optional, Callable
def get_files_info(
    working_directory: str,
    directory: str,
) -> str:
    
    abs_working_dir = os.path.realpath(working_directory)
    target_dir = os.path.realpath(os.path.join(abs_working_dir, directory))
    
    if os.path.commonpath([abs_working_dir, target_dir]) != abs_working_dir:
        return (
            f'Error: Cannot read "{directory}" as it is outside the permitted working directory'
        )
    
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'

    try:
        files_info = []
        for filename in os.listdir(target_dir):
            if filename.startswith("."):
                continue
            filepath = os.path.join(target_dir, filename)
            #file_size = 0 #do not think this is necessary
            #is_dir = os.path.isdir(filepath) #not used and superceded by if not os.path.isfile
            #if is_dir: continue # skip directories with continue
            if not os.path.isfile(filepath):
                continue # skip non-files
            size = os.path.getsize(filepath)
            #files_info.append(f"- file_name={filename} file_size=({size}) bytes, is_dir={is_dir}")
            files_info.append(f"- file_name={filename} file_size=({size}) bytes")
        return "\n".join(files_info)
    except Exception as e: 
        return f"Error listing files: {e}"
    
    
    # if not files_info:
    #     return f"{directory} is empty."
    # return "\n".join(files_info)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory.",
            ),
        },
    ),
)