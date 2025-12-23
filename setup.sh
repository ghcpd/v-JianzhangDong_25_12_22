#!/usr/bin/env bash
set -euo pipefail
# Create fresh venv and install pinned requirements
[ -d .venv ] && printf "Removing existing .venv/\n" && rm -rf .venv
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip setuptools wheel
.venv/bin/python -m pip install -r requirements.txt
printf "Created .venv and installed dependencies.\n"