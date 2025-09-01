# call_function.py
from google.genai import types
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python import run_python_file, schema_run_python_file
from functions.write_file_content import write_file, schema_write_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

functions = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}


def call_function(function_call_part, verbose=False):   
    func_name = function_call_part.name
    raw_args = function_call_part.args if isinstance(function_call_part.args, dict) else {}
    args = dict(raw_args)  # copy
    args["working_directory"] = "./calculator"
    if verbose:
        print(f"Calling function: {func_name}({raw_args})")
    else:
        print(f" - Calling function: {func_name}")
    ...
    func = functions.get(func_name)
    if func is None:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=func_name,
                    response={"error": f"Unknown function: {func_name}"},
                )
            ],
        )
    try:
        function_result = func(**args)
    except Exception as exc:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=func_name,
                    response={"error": f"Exception: {exc}"},
                )
            ],
        )
    print("Function call result:", function_result)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=func_name,
                response={"result": function_result},
            )
        ],
    )