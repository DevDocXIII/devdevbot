# utils.py python
import json
from typing import Any, Dict

def normalize_args(arg: Any) -> Dict[str, Any]:
    """Return a dict from a dict/JSON-string/None; {} on errors."""
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
