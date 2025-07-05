"""
Description: This script builds the Python project using PyInstaller and renames the output executable.
NOTE: This script is intended to be run from the project root directory. Use `python -m build` or `python build/__main__.py` to execute it.
"""

import os
import shutil
import subprocess
from pathlib import Path

# Define directories
ROOT_DIR = Path(__file__).resolve().parent.parent
BUILD_DIR = ROOT_DIR / "build"
DIST_DIR = ROOT_DIR / "dist"
RESOURCES_DIR = ROOT_DIR / "resources"
SRC_DIR = ROOT_DIR / "src"
MAIN_PY = ROOT_DIR / "main.py"
ICON_PATH = RESOURCES_DIR / "icons" / "favicon.ico"
sep = os.sep

print("-" * 40 + f" Building Doro " + "-" * 40)
print(f"Root Directory: {ROOT_DIR}")
print(f"Build Directory: {BUILD_DIR}")
print(f"Distribution Directory: {DIST_DIR}")
print(f"Resources Directory: {RESOURCES_DIR}")
print(f"Source Directory: {SRC_DIR}")
print(f"Main Python File: {MAIN_PY}")
print(f"Icon Path: {ICON_PATH}")
print("-" * 90)

# Remove the last build exe
for exe_name in ["main.exe", "Doro.exe"]:
    exe_path = DIST_DIR / exe_name
    if exe_path.exists():
        exe_path.unlink()

# Activate the doro conda environment before building
activate_env_cmd = "conda activate doro"
os.system(activate_env_cmd)

# Use relative paths for --add-data.
# NOTE: You can edit these
relative_data = map(
    Path,
    [
        r"src\pages\*.html",
    ],
)
add_data_args = [f"{r};{r if r.is_dir() else r.parent}" for r in relative_data]
print(f"Adding data files: {add_data_args}")

pyinstaller_cmd = [
    "pyinstaller",
    # Const arguments
    "--onefile",
    "--clean",
    "-w",
    # Dynamic arguments
    f"--distpath={DIST_DIR}",
    f"--icon={ICON_PATH}",
    f"{MAIN_PY}",
] + [f"--add-data={add_data_arg}" for add_data_arg in add_data_args]

subprocess.run(pyinstaller_cmd, check=True)

# Rename the exe
main_exe = DIST_DIR / "main.exe"
new_exe = DIST_DIR / "Doro.exe"
if main_exe.exists():
    main_exe.rename(new_exe)

# Clear the build directory
for sub in ["__pycache__", "main"]:
    sub_path = BUILD_DIR / sub
    if sub_path.exists():
        if sub_path.is_dir():
            shutil.rmtree(sub_path)
        else:
            sub_path.unlink()

# Remove spec files
for spec_file in [BUILD_DIR / "main.spec", ROOT_DIR / "main.spec"]:
    if spec_file.exists():
        spec_file.unlink()
