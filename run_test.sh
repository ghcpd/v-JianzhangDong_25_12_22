#!/bin/bash

# Test runner script for Linux/macOS
# This script runs all test cases in the tests/ directory

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_DIR/.venv"
TESTS_DIR="$PROJECT_DIR/tests"

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Error: Virtual environment not found at $VENV_DIR"
    echo "Please run setup.sh first to create the environment."
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

echo "=========================================="
echo "Running Tests"
echo "=========================================="
echo "Python: $(python --version)"
echo "pip: $(pip --version)"
echo "Tests Directory: $TESTS_DIR"
echo ""

# Run each test file
cd "$TESTS_DIR"
for test_file in case_*.py; do
    if [ -f "$test_file" ]; then
        echo "Running $test_file..."
        python "$test_file"
        echo "✓ $test_file completed"
        echo ""
    fi
done

echo "=========================================="
echo "All tests completed!"
echo "=========================================="
