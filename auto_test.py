#!/usr/bin/env python3
"""
Run all scripts in the tests/ directory using the project's .venv Python.
Writes results to logs/test_run.log and appends environment info to README.md.
"""
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent
VENV_DIR = ROOT / ".venv"
LOGS_DIR = ROOT / "logs"
LOG_FILE = LOGS_DIR / "test_run.log"
TESTS_DIR = ROOT / "tests"
README = ROOT / "README.md"

# Determine venv python and pip
if os.name == "nt":
    venv_python = VENV_DIR / "Scripts" / "python.exe"
    venv_pip = VENV_DIR / "Scripts" / "pip.exe"
else:
    venv_python = VENV_DIR / "bin" / "python"
    venv_pip = VENV_DIR / "bin" / "pip"

if not venv_python.exists():
    print(".venv/ not found or incomplete. Run setup.sh (or create the venv) before running this script.")
    sys.exit(2)

LOGS_DIR.mkdir(exist_ok=True)

def run_command(cmd, capture_output=True, timeout=300, env=None):
    return subprocess.run(cmd, shell=False, capture_output=capture_output, text=True, timeout=timeout, env=env)

# Gather environment info
py_ver = run_command([str(venv_python), "--version"]).stdout.strip()
pip_ver = run_command([str(venv_pip), "--version"]).stdout.strip()
env_name = ".venv"
abs_path = str(VENV_DIR.resolve())

# Append environment info to README.md
env_info = f"\n\n## Environment snapshot\n- Environment: {env_name}\n- Path: {abs_path}\n- Python: {py_ver}\n- pip: {pip_ver}\n- Generated: {datetime.utcnow().isoformat()}Z\n"
with open(README, "a", encoding="utf-8") as f:
    f.write(env_info)

# Run tests
results = []
for p in sorted(TESTS_DIR.glob("*.py")):
    start = datetime.utcnow()
    # ensure tests can import local `app` package
    child_env = os.environ.copy()
    child_env["PYTHONPATH"] = str(ROOT)
    proc = run_command([str(venv_python), str(p)], env=child_env)
    end = datetime.utcnow()
    results.append({
        "test": p.name,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "duration_seconds": (end - start).total_seconds(),
    })

# Write consolidated log
with open(LOG_FILE, "a", encoding="utf-8") as lf:
    lf.write("# Test run: " + datetime.utcnow().isoformat() + "Z\n")
    lf.write(f"Environment: {env_name}\nPath: {abs_path}\nPython: {py_ver}\nPip: {pip_ver}\n\n")
    for r in results:
        lf.write(f"---\nTest: {r['test']}\nReturn code: {r['returncode']}\nDuration: {r['duration_seconds']}s\n")
        lf.write("Stdout:\n")
        lf.write(r['stdout'] or "<no output>\n")
        lf.write("Stderr:\n")
        lf.write(r['stderr'] or "<no stderr>\n")
        lf.write("\n")

# Exit with non-zero if any test failed
failed = [r for r in results if r['returncode'] != 0]
if failed:
    print(f"{len(failed)} test(s) failed — see {LOG_FILE}")
    sys.exit(1)
print(f"All {len(results)} tests passed. Logs written to {LOG_FILE}")
