@echo off

REM Run test script for Windows
echo Running tests...

REM Activate virtual environment
call .venv\Scripts\activate

REM Run all test scripts in tests\ directory
for %%f in (tests\*.py) do (
    echo Running %%f
    python %%f
)

echo Tests completed.
pause