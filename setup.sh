#!/bin/bash

# Environment setup script for Linux/macOS
# This script creates a virtual environment and installs dependencies

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_DIR/.venv"

echo "=========================================="
echo "Environment Setup for Python Project"
echo "=========================================="
echo "Project Directory: $PROJECT_DIR"
echo "Python Version: $(python3 --version)"
echo "pip Version: $(pip3 --version)"

# Check if .venv exists and remove it
if [ -d "$VENV_DIR" ]; then
    echo "Removing existing virtual environment..."
    rm -rf "$VENV_DIR"
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv "$VENV_DIR"

# Activate virtual environment
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r "$PROJECT_DIR/requirements.txt"

echo "=========================================="
echo "Environment Setup Complete!"
echo "=========================================="
echo ""
echo "To activate the environment, run:"
echo "  source $VENV_DIR/bin/activate"
echo ""
echo "To deactivate the environment, run:"
echo "  deactivate"
echo ""
