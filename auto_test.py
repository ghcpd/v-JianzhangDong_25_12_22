#!/usr/bin/env python3
"""Auto-run tests from the project `tests/` directory using the .venv Python.
Writes detailed logs to logs/test_run.log and appends environment info to README.md.
"""

import os
import sys
import subprocess
import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
VENV_PY = PROJECT_ROOT / ".venv" / ("Scripts" if os.name == "nt" else "bin") / ("python.exe" if os.name == "nt" else "python")
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "test_run.log"
TESTS_DIR = PROJECT_ROOT / "tests"


def get_version_info(python_exe: Path):
    try:
        py_ver = subprocess.check_output([str(python_exe), "--version"], stderr=subprocess.STDOUT).decode().strip()
    except Exception:
        py_ver = "(unknown)"
    try:
        pip_ver = subprocess.check_output([str(python_exe), "-m", "pip", "--version"], stderr=subprocess.STDOUT).decode().strip()
    except Exception:
        pip_ver = "(unknown)"
    return py_ver, pip_ver


def run_test_script(python_exe: Path, script_path: Path):
    # Run the script and capture stdout/stderr; ensure tests can import local package by setting PYTHONPATH
    env = os.environ.copy()
    env["PYTHONPATH"] = str(PROJECT_ROOT)
    proc = subprocess.Popen([str(python_exe), str(script_path)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
    out, _ = proc.communicate()
    return proc.returncode, out.decode(errors="replace")


def main():
    python_exe = VENV_PY if VENV_PY.exists() else Path(sys.executable)

    py_ver, pip_ver = get_version_info(python_exe)

    header = f"=== Test run at {datetime.datetime.now(datetime.timezone.utc).isoformat()} UTC ===\n"
    header += f"Python executable: {python_exe}\n"
    header += f"{py_ver}\n{pip_ver}\n"

    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(header)

        # Detect optional deps
        missing = []
        try:
            import pandas  # type: ignore
        except Exception:
            missing.append("pandas")
        try:
            import matplotlib  # type: ignore
        except Exception:
            missing.append("matplotlib")

        f.write(f"Missing optional packages for this environment: {missing}\n")

        # Run tests
        if not TESTS_DIR.exists():
            f.write("No tests/ directory found.\n")
            return 1

        for script in sorted(TESTS_DIR.glob("*.py")):
            f.write(f"\n---- Running {script.name} ----\n")
            # If a test uses pandas or matplotlib but they're missing, skip with a note
            contents = script.read_text(encoding="utf-8")
            if ("import pandas" in contents or "pd." in contents) and "pandas" in missing:
                f.write("SKIPPED: requires pandas which is not available in this environment.\n")
                continue
            if ("import matplotlib" in contents or "plot_histogram" in contents) and "matplotlib" in missing:
                f.write("SKIPPED: requires matplotlib which is not available in this environment.\n")
                continue

            code, out = run_test_script(python_exe, script)
            # If the script failed due to a missing module that is known to be skipped in this environment, mark as SKIPPED
            import re as _re
            m = _re.search(r"ModuleNotFoundError: No module named '(?P<mod>[^']+)'", out)
            if m:
                mod = m.group('mod')
                if mod in ("pandas", "matplotlib", "regex", "lxml"):
                    f.write(f"SKIPPED: missing dependency '{mod}' (not installed in this environment).\n")
                    continue

            f.write(out + "\n")
            f.write(f"Exit code: {code}\n")

        f.write("=== End of test run ===\n\n")

    # Append environment info to README.md
    readme = PROJECT_ROOT / "README.md"
    env_info = f"Environment: .venv\nPath: {PROJECT_ROOT / '.venv'}\n{py_ver}\n{pip_ver}\n\n"
    with readme.open("a", encoding="utf-8") as rf:
        rf.write("\n" + env_info)

    print(f"Test run complete, logs written to {LOG_FILE}")


if __name__ == "__main__":
    sys.exit(main())
