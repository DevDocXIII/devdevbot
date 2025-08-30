import os
from os import path
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    abs_path = path.abspath(file_path)
    abs_work_dir = path.abspath(working_directory)
    checkfilepath = path.commonpath([abs_path, abs_work_dir]) != abs_work_dir
    if checkfilepath or not os.access(abs_path, os.X_OK):
        raise ValueError(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory or is not executable')
    if not os.access(file_path, os.R_OK):
        raise ValueError(f'Error: File "{file_path}" not found.')
    # Rest of the code...
    if not not file_path.endswith(".py"):
        raise ValueError(f'Error: File "{file_path}" is not a Python script')
    
    subprocess.run(['python', abs_path] + args, cwd=abs_work_dir)