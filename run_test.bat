@echo off
REM Activate venv and run auto_test.py on Windows
if not exist ".venv\Scripts\python.exe" (
  echo No .venv found. Run setup.sh or use: python -m venv .venv && .venv\Scripts\python -m pip install -r requirements.txt
  exit /b 1
)
.venv\Scripts\python.exe auto_test.py
