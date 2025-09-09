# functions/cache.py
import json
from typing import Any, Dict, Tuple, TypedDict

class Payload(TypedDict, total=False):
    status: str
    kind: str
    details: str
    artifacts: Dict[str, Any]

def make_key(name: str, args: Dict[str, Any]) -> str:
    try:
        args_str = json.dumps(args, sort_keys=True, separators=(',', ':'))
    except TypeError:
        # Fallback: convert non-serializable values to strings
        safe_args = {k: (v if isinstance(v, (str, int, float, bool, list, dict, type(None))) else str(v)) for k, v in args.items()}
        args_str = json.dumps(safe_args, sort_keys=True, separators=(',', ':'))
    return f"{name}|{args_str}"

class ToolCache:
    def __init__(self) -> None:
        self._parts: Dict[str, Any] = {}      # cached function_response Part
        self._payloads: Dict[str, Dict] = {}  # cached response payload dict

    def get(self, name: str, args: Dict[str, Any]) -> Tuple[Any, Dict[str, Any]]:
        key = make_key(name, args)
        return self._parts.get(key, None), self._payloads.get(key, {})

    def set(self, name: str, args: Dict[str, Any], resp_part: Any, payload: Dict) -> None:
        key = make_key(name, args)
        self._parts[key] = resp_part
        self._payloads[key] = payload