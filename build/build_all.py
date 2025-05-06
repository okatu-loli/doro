import os
import subprocess
import re
from typing import List, Tuple


def main():
    current_dir: str = os.path.dirname(os.path.abspath(__file__))

    python_files = [
        f
        for f in os.listdir(current_dir)
        if f.endswith(".py") and f != os.path.basename(__file__)
    ]

    execution_order: List[Tuple[int, str]] = []

    for py_file in python_files:
        file_path = os.path.join(current_dir, py_file)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            match = re.search(r"\[#ExecutionOrder\s*=\s*(\d+)\]", content)
            if match:
                order = int(match.group(1))
                execution_order.append((order, py_file))

    execution_order.sort(key=lambda x: x[0])

    for order, py_file in execution_order:
        file_path = os.path.join(current_dir, py_file)
        print(f"Order: {order}, Running {py_file}...")
        subprocess.run(["python", file_path])


if __name__ == "__main__":
    main()
