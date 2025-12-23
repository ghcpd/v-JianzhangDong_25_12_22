@echo off
set VENV=.venv\Scripts\python.exe
if not exist "%VENV%" (
  echo .venv not found — run setup.bat or setup.sh first.
  exit /b 2
)
if not exist logs mkdir logs
echo Running tests using %VENV%> logs\test_run.log
for %%F in (tests\*.py) do (
  echo --- Running %%F --- >> logs\test_run.log
  "%VENV%" "%%F" >> logs\test_run.log 2>&1 || echo %%F exited with non-zero status >> logs\test_run.log
)
echo Tests finished — see logs\test_run.log
