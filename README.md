# Python Dependency Management Project

## Overview

This project demonstrates comprehensive dependency management and maintenance practices for Python projects. It includes vulnerability analysis, version updates, environment setup scripts, and automated testing infrastructure.

## Generated Files & Purpose

### Configuration & Documentation
- **requirements.txt** - Updated dependencies with secure, stable, and Python 3.14-compatible versions
- **requirements_backup.txt** - Original requirements for reference and rollback
- **report.json** - Detailed vulnerability analysis and dependency update report
- **README.md** - This file, providing setup and usage instructions
- **.gitignore** - Git configuration to exclude virtual environments and generated files

### Environment Setup Scripts
- **Dockerfile** - Docker image definition for containerized environment
- **setup.sh** - Bash script for Linux/macOS virtual environment setup
- **run_test.sh** - Bash script to execute tests on Linux/macOS

### Windows Scripts
- **run_test.bat** - Batch script to execute tests on Windows

### Python Scripts
- **auto_test.py** - Automatic test runner with environment detection
  - Automatically detects and runs all test cases in `tests/` directory
  - Generates detailed logs with environment information
  - Outputs results to `logs/test_run.log`

### Project Structure
- **.venv/** - Python 3.14 virtual environment with all dependencies installed
- **app/** - Application source code
  - `__init__.py` - Package initialization
  - `data_loader.py` - CSV/YAML data loading utilities
  - `text_processor.py` - Text processing functionality
  - `visualizer.py` - Data visualization utilities
- **tests/** - Test cases
  - `case_1.py` - Data loading tests
  - `case_2.py` - Text processing tests
  - `case_3.py` - Visualization and XML parsing tests
- **logs/** - Test execution logs
  - `test_run.log` - Detailed test results with environment info

## Environment Information

- **Python Version**: Python 3.14.0
- **Pip Version**: pip 25.3
- **Virtual Environment Path**: `.venv/`
- **Platform**: Windows

## Dependencies

All dependencies have been updated to Python 3.14-compatible versions:

| Package | Original | Updated | Status |
|---------|----------|---------|--------|
| numpy | 1.24.0 | 2.4.0 | ✓ Secure |
| pandas | 1.5.0 | 2.3.3 | ✓ Secure |
| matplotlib | 3.5.0 | 3.10.8 | ✓ Secure |
| scipy | 1.9.0 | 1.16.3 | ✓ Secure |
| requests | 2.25.0 | 2.32.5 | ✓ Secure |
| pyyaml | 5.3.1 | 6.0.3 | ✓ Secure |
| regex | 2021.4.4 | 2025.11.3 | ✓ Secure |
| tqdm | 4.32.0 | 4.67.1 | ✓ Secure |
| lxml | 4.6.1 | 6.0.2 | ✓ Secure |
| typing_extensions | 3.7.4 | 4.15.0 | ✓ Secure |
## Setup Instructions

### Prerequisites
- Python 3.14.0 or later
- pip 25.0 or later
- Git (optional, for version control)

### Option 1: Using setup.sh (Linux/macOS)

```bash
# Make the setup script executable
chmod +x setup.sh

# Run the setup script
./setup.sh

# Activate the environment
source .venv/bin/activate
```

### Option 2: Using setup.bat (Windows)

```batch
REM Run the setup batch script
setup.bat

REM The environment will be created at .venv\
```

### Option 3: Manual Setup

```bash
# Create virtual environment
python -m venv .venv

# Activate the environment (Windows)
.\.venv\Scripts\activate

# Activate the environment (Linux/macOS)
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

## Running Tests

### Using auto_test.py (Recommended)

The `auto_test.py` script automatically detects your environment and runs all tests:

```bash
# Run all tests with automatic environment detection
python auto_test.py
```

This will:
1. Detect the Python interpreter from `.venv/`
2. Set up the Python path to include the project directory
3. Execute all `case_*.py` test files
4. Generate a detailed log in `logs/test_run.log`

### Using run_test.sh (Linux/macOS)

```bash
# Make the script executable
chmod +x run_test.sh

# Run tests
./run_test.sh
```

### Using run_test.bat (Windows)

```batch
# Run tests
run_test.bat
```

### Manual Test Execution

```bash
# Activate the virtual environment first
source .venv/bin/activate  # Linux/macOS
.\.venv\Scripts\activate   # Windows

# Run individual tests
python tests/case_1.py
python tests/case_2.py
python tests/case_3.py
```

## Checking Test Logs

Test results are automatically written to `logs/test_run.log`:

```bash
# View the test log
cat logs/test_run.log        # Linux/macOS
type logs\test_run.log       # Windows

# View last 50 lines of the log
tail -50 logs/test_run.log   # Linux/macOS
```

The log file contains:
- Test execution timestamp
- Python version and pip version information
- Platform details
- Individual test results (PASSED/FAILED)
- Standard output and error messages from each test
- Summary statistics (total tests, passed, failed, success rate)

## Dependency Analysis

For detailed vulnerability analysis and update justifications, see [report.json](report.json).

The analysis identified and updated 10 packages with:
- Known security vulnerabilities
- Incompatibilities with Python 3.14
- Deprecated or unsupported versions

## Using Docker

If you prefer a containerized environment:

```bash
# Build the Docker image
docker build -t python-dependency-project .

# Run tests in the container
docker run --rm python-dependency-project
```

## Deactivating the Virtual Environment

```bash
# Linux/macOS
deactivate

# Windows (Command Prompt)
.venv\Scripts\deactivate.bat
```

## Troubleshooting

### Module Import Errors

If tests fail with "ModuleNotFoundError: No module named 'app'":
- Ensure the virtual environment is activated
- Verify you're running tests from the project root directory
- Check that `PYTHONPATH` includes the project directory (auto_test.py handles this)

### Missing Dependencies

If packages are missing:
```bash
# Reinstall all dependencies
pip install -r requirements.txt --force-reinstall
```

### Virtual Environment Issues

If the `.venv/` directory is corrupted:
```bash
# Remove and recreate the environment
rm -rf .venv              # Linux/macOS
rmdir /s /q .venv         # Windows
python -m venv .venv
pip install -r requirements.txt
```

## Best Practices

1. **Always use virtual environments** - Isolates project dependencies
2. **Pin specific versions** - Prevents unexpected breaking changes
3. **Regular updates** - Keep dependencies current for security
4. **Automated testing** - Run tests before and after updates
5. **Document changes** - Maintain a changelog via report.json
6. **Git ignore .venv** - Don't commit virtual environment to version control

## Security Notes

- All dependencies have been updated to remove known vulnerabilities
- PyYAML updated from 5.3.1 (CVE-2020-14343) to 6.0.3
- Requests updated from 2.25.0 (CVE-2023-32681) to 2.32.5
- Regular dependency audits recommended with `pip-audit`

## License & Attribution

Generated as part of dependency maintenance engineering process.
Date: December 22, 2025

## Setup Instructions
