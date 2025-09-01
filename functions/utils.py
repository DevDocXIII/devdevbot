# functions/utils.py
import json
from typing import Any, Dict

def normalize_args(arg: Any) -> Dict[str, Any]:
    if isinstance(arg, dict):
        return arg
    if not arg:
        return {}
    # Some SDK objects expose to_json()
    to_json = getattr(arg, "to_json", None)
    if callable(to_json):
        val = to_json()
        return val if isinstance(val, dict) else {}
    if isinstance(arg, str):
        try:
            val = json.loads(arg)
            return val if isinstance(val, dict) else {}
        except json.JSONDecodeError:
            return {}
    return {}