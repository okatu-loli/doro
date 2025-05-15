import os
import sys
from typing import Any, Dict


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


def get_current_location():
    if getattr(sys, "frozen", False):
        return os.path.dirname(os.path.abspath(sys.executable))
    else:
        return os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))


REFL_MAP = {
    "ROOT": get_current_location(),  # 根目录
}
