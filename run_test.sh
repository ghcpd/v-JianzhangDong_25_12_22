#!/usr/bin/env bash
set -euo pipefail
PYTHON=.venv/bin/python
if [ ! -x "$PYTHON" ]; then
  echo ".venv not found or missing interpreter — run ./setup.sh first." >&2
  exit 2
fi
mkdir -p logs
echo "Running tests using $PYTHON" > logs/test_run.log
for f in tests/*.py; do
  echo "--- Running $f ---" | tee -a logs/test_run.log
  "$PYTHON" "$f" 2>&1 | tee -a logs/test_run.log || echo "$f exited with non-zero status" | tee -a logs/test_run.log
done
echo "Tests finished — see logs/test_run.log"