#!/usr/bin/env bash
set -euo pipefail

# Create a fresh virtualenv at .venv/ and install pinned deps
if [ -d ".venv" ]; then
  echo "Removing existing .venv/"
  rm -rf .venv
fi

python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

echo "Virtual environment created at $(pwd)/.venv and dependencies installed."
