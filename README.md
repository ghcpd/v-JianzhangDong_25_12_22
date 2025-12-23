# Project environment & test helpers

This repository has been updated with automated environment and test helpers.

Generated files (purpose) ✅

- `requirements_backup.txt` — original requirements (unchanged)
- `requirements.txt` — **pinned, secure** dependencies (created from a clean `.venv`)
- `report.json` — simplified dependency update report
- `.gitignore` — ignores `.venv/`, logs, caches
- `.venv/` — fresh virtual environment (DO NOT commit)
- `setup.sh` — create `.venv` and install dependencies (Linux/macOS)
- `run_test.sh` — run tests using `.venv` (Linux/macOS)
- `run_test.bat` — run tests using `.venv` (Windows)
- `auto_test.py` — programmatic runner that uses `.venv` Python and writes `logs/test_run.log`
- `Dockerfile` — container reproducer that installs `requirements.txt` and runs tests
- `logs/test_run.log` — test run output (created when tests are executed)

Quick start — Linux / macOS ✅

1. Create environment and install dependencies:
   ./setup.sh
2. Run tests:
   ./run_test.sh
3. Or run the automated tester (uses `.venv`):
   .venv/bin/python auto_test.py

Quick start — Windows ✅

1. Create environment:
   python -m venv .venv
   .venv\Scripts\python -m pip install --upgrade pip setuptools wheel
   .venv\Scripts\python -m pip install -r requirements.txt
2. Run tests:
   run_test.bat
3. Or run the automated tester:
   .venv\Scripts\python auto_test.py

How to inspect results 🔎

- Test output is appended to `logs/test_run.log`.
- `report.json` describes the dependency updates and reasons.

Notes & troubleshooting ⚠️

- `.venv/` is intentionally gitignored.
- If dependency installation fails, check your network and retry `./setup.sh`.

---

Environment: .venv
Absolute path: D:\projects\v-JianzhangDong_25_12_22\oswe-mini-m23a1s255\v-JianzhangDong_25_12_22\.venv
Python 3.14.0 | pip 25.3 from D:\projects\v-JianzhangDong_25_12_22\oswe-mini-m23a1s255\v-JianzhangDong_25_12_22\.venv\Lib\site-packages\pip (python 3.14)

---

Environment: .venv
Absolute path: D:\projects\v-JianzhangDong_25_12_22\oswe-mini-m23a1s255\v-JianzhangDong_25_12_22\.venv
Python 3.14.0 | pip 25.3 from D:\projects\v-JianzhangDong_25_12_22\oswe-mini-m23a1s255\v-JianzhangDong_25_12_22\.venv\Lib\site-packages\pip (python 3.14)
