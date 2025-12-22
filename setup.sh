#!/bin/bash

# Setup script for Linux/macOS
echo "Setting up virtual environment..."

# Remove existing .venv if it exists
if [ -d ".venv" ]; then
    rm -rf .venv
fi

# Create new virtual environment
python3 -m venv .venv

# Activate and install dependencies
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Setup complete."