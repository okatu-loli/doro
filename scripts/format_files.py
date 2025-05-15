"""
[#name = format]
"""

import os
import black
from black.report import NothingChanged


def format_file_with_black(file_path: str) -> None:
    with open(file_path, "r", encoding="utf-8") as file:
        source_code = file.read()

    try:
        formatted_code = black.format_file_contents(
            source_code, fast=False, mode=black.FileMode()
        )
    except NothingChanged:
        return
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(formatted_code)


def format_files_in_directory(directory: str) -> None:
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                format_file_with_black(file_path)


def main():
    current_directory = os.getcwd()
    format_files_in_directory(current_directory)
    print("All Python files have been formatted.")


if __name__ == "__main__":
    main()
