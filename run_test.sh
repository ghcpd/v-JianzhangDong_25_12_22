#!/bin/bash

# Run test script for Linux/macOS
echo "Running tests..."

# Activate virtual environment
source .venv/bin/activate

# Run all test scripts in tests/ directory
for test_file in tests/*.py; do
    if [ -f "$test_file" ]; then
        echo "Running $test_file"
        python "$test_file"
    fi
done

echo "Tests completed."