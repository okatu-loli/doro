@REM Description: This script builds the Python project using PyInstaller and renames the output executable.
@REM NOTE: This script is intended to be run from the project root directory.

@echo off
setlocal enabledelayedexpansion

@REM Define the directories
set "CURRENT_DIR=%~dp0"
for %%I in ("%CURRENT_DIR%\..") do set "ROOT_DIR=%%~fI"
set "BUILD_DIR=%ROOT_DIR%\build"
set "PYTHON_DIR=%ROOT_DIR%\python"
set "DIST_DIR=%ROOT_DIR%\dist"
set "RESOURCES_DIR=%ROOT_DIR%\resources"

@REM Remove the last build exe
del "%DIST_DIR%\main.exe"
del "%DIST_DIR%\Doro.exe"

@REM Run the build script
call pyinstaller.exe --onefile -w --distpath %DIST_DIR% --icon=%RESOURCES_DIR%\icons\favicon.ico %ROOT_DIR%\main.py --clean

@REM Rename the exe
set "EXE_NAME=main.exe"
set "NEW_EXE_NAME=Doro.exe"
rename "%DIST_DIR%\%EXE_NAME%" "%NEW_EXE_NAME%"

@REM Clear the build directory
rmdir /s /q %BUILD_DIR%\__pycache__
rmdir /s /q %BUILD_DIR%\main
del /f %BUILD_DIR%\main.spec
del /f %ROOT_DIR%\main.spec
