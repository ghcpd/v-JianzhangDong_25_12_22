@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

REM Activate .venv and run auto_test.py
if not exist ".venv\Scripts\activate.bat" (
  echo .venv\Scripts\activate.bat not found. Run setup with Python first.
  exit /b 1
)

call .venv\Scripts\activate.bat
python auto_test.py
