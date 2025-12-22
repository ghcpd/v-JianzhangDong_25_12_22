#!/usr/bin/env bash
set -euo pipefail

# Activate .venv and run auto_test.py
if [ ! -d ".venv" ]; then
  echo "No .venv found. Run setup.sh first to create the environment."
  exit 1
fi

. .venv/bin/activate
python auto_test.py
