@echo off
REM Test runner script for Windows
REM This script runs all test cases in the tests\ directory

setlocal enabledelayedexpansion

set "PROJECT_DIR=%~dp0"
set "VENV_DIR=%PROJECT_DIR%.venv"
set "TESTS_DIR=%PROJECT_DIR%tests"
set "PYTHON_EXE=%VENV_DIR%\Scripts\python.exe"

REM Check if virtual environment exists
if not exist "%VENV_DIR%" (
    echo Error: Virtual environment not found at %VENV_DIR%
    echo Please run setup.bat first to create the environment.
    exit /b 1
)

echo ==========================================
echo Running Tests
echo ==========================================
for /f "tokens=*" %%i in ('"%PYTHON_EXE%" --version') do set "PYTHON_VERSION=%%i"
for /f "tokens=*" %%i in ('"%VENV_DIR%\Scripts\pip.exe" --version') do set "PIP_VERSION=%%i"

echo Python: %PYTHON_VERSION%
echo pip: %PIP_VERSION%
echo Tests Directory: %TESTS_DIR%
echo.

REM Run each test file
cd /d "%TESTS_DIR%"
for %%f in (case_*.py) do (
    echo Running %%f...
    "%PYTHON_EXE%" "%%f"
    if !errorlevel! equ 0 (
        echo ^✓ %%f completed
    ) else (
        echo ^✗ %%f failed with error code !errorlevel!
    )
    echo.
)

echo ==========================================
echo All tests completed!
echo ==========================================
pause
