#!/usr/bin/env bash
set -euo pipefail

# Create a fresh virtual environment and install pinned dependencies
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENVDIR="$PROJECT_ROOT/.venv"

if [ -d "$VENVDIR" ]; then
  echo "Removing existing .venv/"
  rm -rf "$VENVDIR"
fi

python3 -m venv "$VENVDIR"
source "$VENVDIR/bin/activate"
python -m pip install --upgrade pip setuptools wheel
pip install -r "$PROJECT_ROOT/requirements.txt"

echo "Environment created at $VENVDIR"
