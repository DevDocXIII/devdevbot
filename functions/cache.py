# functions/cache.py
import json
from typing import Any, Dict, Tuple,TypedDict
class Payload(TypedDict, total=False):
    status: str
    kind: str
    details: str
    artifacts: Dict[str, Any]

def make_key(name: str, args: Dict[str, Any]) -> str:
    return f"{name}|{json.dumps(args, sort_keys=True, separators=(',', ':'))}"

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