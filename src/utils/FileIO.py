import json
from typing import Any

from .EnvConsts import replace_map


def json_load(file_path: str, replace: bool = True) -> Any:
    try:
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)
            if replace:
                replace_map(data)
            return data
    except Exception:
        return None


def json_dump(file_path: str, data: Any) -> None:
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
