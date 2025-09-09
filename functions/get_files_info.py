# funtions/get_files_info.py
from google.genai import types
import os
from typing import Any, Dict, List, Optional, Callable

# Function to list files in a directory with security checks
def get_files_info(working_directory: str, directory: str = ".") ->dict:
    
    # Get the absolute path of the working directory
    abs_working_dir = os.path.realpath(working_directory)
    # Get the absolute path of the target directory
    target_dir = os.path.realpath(os.path.join(abs_working_dir, directory))
    
    # Check if the target directory is within the allowed working directory
    if os.path.commonpath([abs_working_dir, target_dir]) != abs_working_dir:
        return {"status":"error","kind":"list","details":"outside working dir"}
    
    # Verify that the target is actually a directory
    if not os.path.isdir(target_dir):
        return {"status":"error","kind":"list","details":f'not a directory: "{directory}"'}

    # Initialize list to store directory entries
    entries = []
    # Iterate through sorted directory contents
    for name in sorted(os.listdir(target_dir)):
        p = os.path.join(target_dir, name)
        entries.append({
            "name": name,
            "is_dir": os.path.isdir(p),
            "size": os.path.getsize(p) if os.path.isfile(p) else None,
        })
    
    # Return successful response with directory listing
    return {"status":"ok","kind":"list","artifacts":{"directory": directory, "entries": entries}}

# Schema definition for the function declaration
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