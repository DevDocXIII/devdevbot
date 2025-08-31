# utils.py python
import json

def normalize_args(arg):
    if isinstance(arg, dict):
        return arg
    if not arg:
        return {}
    if isinstance(arg, str):
        try:
            out = json.loads(arg)
            return out if isinstance(out, dict) else {}
        except json.JSONDecodeError:
            return {}
    return {}
