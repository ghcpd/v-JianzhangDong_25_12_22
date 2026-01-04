#!/usr/bin/env python
"""
Auto Test Runner - Automatically detects and runs all test cases
This script uses the .venv/ environment to execute all test scripts
and logs results to logs/test_run.log
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
from datetime import datetime


def get_venv_python_executable():
    """Get the Python executable path from the .venv directory"""
    project_dir = Path(__file__).parent.absolute()
    venv_dir = project_dir / ".venv"
    
    if platform.system() == "Windows":
        python_exe = venv_dir / "Scripts" / "python.exe"
    else:
        python_exe = venv_dir / "bin" / "python"
    
    if not python_exe.exists():
        print(f"Error: Virtual environment not found at {venv_dir}")
        print("Please run setup.sh (Linux/macOS) or setup.bat (Windows) first.")
        sys.exit(1)
    
    return str(python_exe)


def get_python_version(python_exe):
    """Get Python version"""
    try:
        result = subprocess.run(
            [python_exe, "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return "Unknown"


def get_pip_version(python_exe):
    """Get pip version"""
    try:
        result = subprocess.run(
            [python_exe, "-m", "pip", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return "Unknown"


def setup_logs_directory():
    """Create logs directory if it doesn't exist"""
    project_dir = Path(__file__).parent.absolute()
    logs_dir = project_dir / "logs"
    logs_dir.mkdir(exist_ok=True)
    return logs_dir


def run_tests(python_exe, venv_dir):
    """Run all test cases and return results"""
    project_dir = Path(__file__).parent.absolute()
    tests_dir = project_dir / "tests"
    logs_dir = setup_logs_directory()
    log_file = logs_dir / "test_run.log"
    
    if not tests_dir.exists():
        print(f"Error: Tests directory not found at {tests_dir}")
        sys.exit(1)
    
    # Get environment info
    python_version = get_python_version(python_exe)
    pip_version = get_pip_version(python_exe)
    
    # Prepare log content
    log_content = []
    log_content.append("=" * 60)
    log_content.append(f"Test Run Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log_content.append("=" * 60)
    log_content.append("")
    log_content.append("Environment Information:")
    log_content.append(f"  Project Directory: {project_dir}")
    log_content.append(f"  Virtual Environment: {venv_dir}")
    log_content.append(f"  Python Version: {python_version}")
    log_content.append(f"  Pip Version: {pip_version}")
    log_content.append(f"  Platform: {platform.system()} {platform.release()}")
    log_content.append("")
    log_content.append("=" * 60)
    log_content.append("Test Results:")
    log_content.append("=" * 60)
    log_content.append("")
    
    # Find and run all test files
    test_files = sorted(tests_dir.glob("case_*.py"))
    total_tests = len(test_files)
    passed_tests = 0
    failed_tests = 0
    
    if total_tests == 0:
        log_content.append("No test files found (looking for case_*.py)")
    else:
        print(f"Found {total_tests} test file(s)")
        
        for test_file in test_files:
            print(f"\nRunning {test_file.name}...", end=" ")
            log_content.append(f"\n[Test] {test_file.name}")
            log_content.append("-" * 60)
            
            try:
                # Set up environment with project directory in PYTHONPATH
                env = os.environ.copy()
                env["PYTHONPATH"] = str(project_dir)
                
                result = subprocess.run(
                    [python_exe, str(test_file)],
                    capture_output=True,
                    text=True,
                    check=False,
                    cwd=str(project_dir),
                    env=env
                )
                
                if result.returncode == 0:
                    print("✓ PASSED")
                    passed_tests += 1
                    log_content.append("Status: PASSED")
                else:
                    print("✗ FAILED")
                    failed_tests += 1
                    log_content.append("Status: FAILED")
                
                if result.stdout:
                    log_content.append("\nStdout:")
                    log_content.append(result.stdout)
                
                if result.stderr:
                    log_content.append("\nStderr:")
                    log_content.append(result.stderr)
                
            except Exception as e:
                print("✗ ERROR")
                failed_tests += 1
                log_content.append(f"Status: ERROR - {str(e)}")
            
            log_content.append("")
    
    # Summary
    log_content.append("=" * 60)
    log_content.append("Test Summary:")
    log_content.append("=" * 60)
    log_content.append(f"Total Tests: {total_tests}")
    log_content.append(f"Passed: {passed_tests}")
    log_content.append(f"Failed: {failed_tests}")
    log_content.append(f"Success Rate: {(passed_tests/total_tests*100) if total_tests > 0 else 0:.1f}%")
    log_content.append("")
    log_content.append(f"Log file: {log_file}")
    log_content.append("")
    
    # Write to log file
    with open(log_file, "w", encoding="utf-8") as f:
        f.write("\n".join(log_content))
    
    print(f"\n{'=' * 60}")
    print(f"Test Summary: {passed_tests} passed, {failed_tests} failed out of {total_tests} tests")
    print(f"Logs written to: {log_file}")
    print(f"{'=' * 60}")
    
    return failed_tests == 0


def main():
    """Main entry point"""
    print("Auto Test Runner - Python 3.14")
    print("=" * 60)
    
    # Get virtual environment Python executable
    python_exe = get_venv_python_executable()
    venv_dir = Path(python_exe).parent.parent
    
    print(f"Using Python: {python_exe}")
    print(f"Environment: {venv_dir}")
    print("")
    
    # Run tests
    success = run_tests(python_exe, venv_dir)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
