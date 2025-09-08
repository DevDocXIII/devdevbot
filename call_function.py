# call_function.py
from typing import Any, Dict
from google.genai import types
from config import WORKING_DIRECTORY
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python import run_python_file, schema_run_python_file
from functions.write_file_content import write_file, schema_write_file
from functions.utils import normalize_args

function_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file
}

expected_keys = {
    "file_path",     # for write_file, get_file_content, …
    "directory",     # for get_files_info
    "content",       # for write_file
    "working_directory",

}
arg_whitelists = {
    "get_files_info": {"working_directory", "directory"},
    "get_file_content": {"working_directory", "file_path"},
    "run_python_file": {"working_directory", "file_path", "args"},
    "write_file": {"working_directory", "file_path", "content"},
}


def _filter_args(expected_keys: set[str], supplied: dict[str, Any]) -> dict[str, Any]:
    filtered = {}
    for k in expected_keys:
        if k in supplied:
            filtered[k] = supplied[k]
    # silently drop any extra keys – they are ignored by the helper
    return filtered

    # 3️⃣ Build the argument dictionary that the helper actually expects


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

def call_function(function_call_part, verbose=False):   
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    # ---------------------------------------------------------------- #
    # 1️⃣ Normalise and inject the sandbox root
    # ---------------------------------------------------------------- #
    
    supplied = normalize_args(function_call_part.args)
    supplied["working_directory"] = WORKING_DIRECTORY  

    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file
    }

    expected_keys = {
      "file_path",     # for write_file, get_file_content, …
      "directory",     # for get_files_info
      "content",       # for write_file
      "working_directory",

    }
    arg_whitelists = {
        "get_files_info": {"working_directory", "directory"},
        "get_file_content": {"working_directory", "file_path"},
        "run_python_file": {"working_directory", "file_path", "args"},
        "write_file": {"working_directory", "file_path", "content"},
    }

    function_name = function_call_part.name
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    # ----------------------------------------------------------- #
    # 2️⃣ Prepare the *filtered* arguments for the helper
    # ----------------------------------------------------------- #
    function_name = function_call_part.name
    if function_name not in function_map:
        payload = {"status": "error", "kind": function_name, "details": "Unknown function"}
    else:
        filtered_args = {k: v for k, v in supplied.items() if k in arg_whitelists[function_name]}
        try:
            raw = function_map[function_name](**filtered_args)
            payload = raw if isinstance(raw, dict) else {
                "status": "ok",
                "kind": function_name,
                "details": str(raw),
            }
        except Exception as exc:
            payload = {"status": "error", "kind": function_name, "details": f"Exception: {exc}"}

    return types.Content(
        role="tool",
        parts=[types.Part.from_function_response(name=function_name, response=payload)],
    )
    
