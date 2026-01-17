#!/usr/bin/env bash
set -euo pipefail

# Activate virtualenv and run auto_test.py
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENVDIR="$PROJECT_ROOT/.venv"

if [ ! -d "$VENVDIR" ]; then
  echo ".venv/ not found — run setup.sh first"
  exit 1
fi

source "$VENVDIR/bin/activate"
python auto_test.py
