import os
from typing import Any, Dict


REFL_MAP = {
    "PROJECT_ROOT": os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ),  # 项目根目录
}


def replace_map(iterable: Dict[Any, Any]) -> None:
    for key, value in iterable.items():
        if hasattr(value, "__iter__") and not isinstance(value, str):
            replace_map(value)
        elif isinstance(value, str):
            for ref_key, ref_value in REFL_MAP.items():
                if ref_key in value:
                    iterable[key] = value.replace("{" + ref_key + "}", ref_value)
                    break
