import os
from typing import Any, Dict


REFL_MAP = {
    "PROJECT_ROOT": os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ),  # 项目根目录
}


def replace_map(iterable: Dict[Any, Any]) -> None:
    for key, value in iterable.items():
        if isinstance(value, str):
            for ref_key, ref_value in REFL_MAP.items():
                if f"{{{ref_key}}}" in value:
                    iterable[key] = value.replace(f"{{{ref_key}}}", ref_value)
        elif hasattr(value, "__iter__"):
            replace_map(value)
        elif isinstance(value, (int, float, bool)):
            pass
        else:
            raise TypeError(f"Unsupported type: {type(value)}")
