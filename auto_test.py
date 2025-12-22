#!/usr/bin/env python3
"""
auto_test.py - Automated testing script for the project.

This script activates the virtual environment under .venv/,
runs all test scripts in the tests/ directory,
and logs the results to logs/test_run.log.
It also appends environment information to README.md.
"""

import os
import sys
import subprocess
import datetime

def main():
    # Define paths
    venv_python = os.path.join('.venv', 'Scripts', 'python.exe') if os.name == 'nt' else os.path.join('.venv', 'bin', 'python')
    tests_dir = 'tests'
    log_file = os.path.join('logs', 'test_run.log')
    readme_file = 'README.md'

    # Ensure log directory exists
    os.makedirs('logs', exist_ok=True)

    # Get environment info
    try:
        python_version = subprocess.check_output([venv_python, '--version'], text=True).strip()
        pip_version = subprocess.check_output([venv_python, '-m', 'pip', '--version'], text=True).strip().split()[1]
        env_name = '.venv'
        env_path = os.path.abspath('.venv')
    except subprocess.CalledProcessError as e:
        print(f"Error getting environment info: {e}")
        return

    # Run tests
    with open(log_file, 'w') as log:
        log.write(f"Test run started at {datetime.datetime.now()}\n")
        log.write(f"Python version: {python_version}\n")
        log.write(f"Pip version: {pip_version}\n\n")

        if not os.path.exists(tests_dir):
            log.write(f"Tests directory '{tests_dir}' not found.\n")
            return

        test_files = [f for f in os.listdir(tests_dir) if f.endswith('.py')]
        if not test_files:
            log.write("No test files found in tests/ directory.\n")
            return

        for test_file in test_files:
            test_path = os.path.join(tests_dir, test_file)
            log.write(f"Running {test_file}...\n")
            try:
                env = os.environ.copy()
                env['PYTHONPATH'] = os.getcwd()
                result = subprocess.run([venv_python, test_path], capture_output=True, text=True, timeout=60, env=env)
                log.write(f"STDOUT:\n{result.stdout}\n")
                if result.stderr:
                    log.write(f"STDERR:\n{result.stderr}\n")
                log.write(f"Return code: {result.returncode}\n\n")
            except subprocess.TimeoutExpired:
                log.write("Test timed out.\n\n")
            except Exception as e:
                log.write(f"Error running test: {e}\n\n")

        log.write(f"Test run completed at {datetime.datetime.now()}\n")

    # Append to README.md
    with open(readme_file, 'a') as readme:
        readme.write(f"\n## Environment Information\n")
        readme.write(f"- Environment Name: {env_name}\n")
        readme.write(f"- Absolute Path: {env_path}\n")
        readme.write(f"- Python Version: {python_version}\n")
        readme.write(f"- Pip Version: {pip_version}\n")

    print(f"Tests completed. Results logged to {log_file}")
    print(f"Environment info appended to {readme_file}")

if __name__ == "__main__":
    main()