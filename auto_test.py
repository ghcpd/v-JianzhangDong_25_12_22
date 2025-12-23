#!/usr/bin/env python3
"""Faster test runner: execute test scripts from `tests/` using the project's .venv Python.

Improvements over the original:
- Runs test scripts in parallel (configurable) to reduce total wall time
- Keeps isolation by invoking the .venv interpreter for each script
- Records per-test duration and exit codes
- Backward-compatible logging and README append behavior
"""
from __future__ import annotations
import argparse
import concurrent.futures
import os
import sys
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VENV_PY = ROOT / '.venv' / ('Scripts' if os.name == 'nt' else 'bin') / ('python.exe' if os.name == 'nt' else 'python')
LOGS = ROOT / 'logs'
LOG_FILE = LOGS / 'test_run.log'
README = ROOT / 'README.md'


def run_one(test_path: Path) -> dict:
    """Run a single test script with the .venv Python and return a result dict.

    Ensure the project root is on PYTHONPATH so `import app` (sibling package) works
    when the test is executed as a script (common cause of ModuleNotFoundError).
    """
    start = time.perf_counter()
    env = os.environ.copy()
    # Ensure the project root is visible to the test subprocess
    env.setdefault('PYTHONPATH', str(ROOT))
    proc = subprocess.run(
        [str(VENV_PY), str(test_path)],
        capture_output=True,
        text=True,
        env=env,
        cwd=str(ROOT),
    )
    duration = time.perf_counter() - start
    # Helpful diagnostic when import fails quickly
    if proc.returncode != 0 and 'ModuleNotFoundError' in (proc.stderr or ''):
        proc.stderr = (proc.stderr or '') + f"\n(Hint: PYTHONPATH={ROOT} was set for this run)"
    return {
        'name': test_path.name,
        'path': str(test_path),
        'stdout': proc.stdout,
        'stderr': proc.stderr,
        'rc': proc.returncode,
        'duration': round(duration, 3),
    }


def main(argv: list[str]) -> int:
    if not VENV_PY.exists():
        print('.venv not found. Run ./setup.sh to create the environment.', file=sys.stderr)
        return 2

    parser = argparse.ArgumentParser(description='Run tests from tests/ using .venv Python')
    parser.add_argument('--workers', '-w', type=int, default=max(1, min(4, (os.cpu_count() or 1))),
                        help='maximum parallel workers (default: min(4, CPU))')
    parser.add_argument('--sequential', action='store_true', help='run tests sequentially')
    args = parser.parse_args(argv)

    LOGS.mkdir(exist_ok=True)
    tests = sorted((ROOT / 'tests').glob('*.py'))
    if not tests:
        print('No tests found in tests/ — nothing to do.')
        return 0

    results: list[dict] = []
    if args.sequential or args.workers == 1:
        for t in tests:
            results.append(run_one(t))
    else:
        # Use threads to avoid extra Python process overhead; subprocesses run the heavy work.
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as ex:
            futures = {ex.submit(run_one, t): t for t in tests}
            for fut in concurrent.futures.as_completed(futures):
                results.append(fut.result())

    # Write results in filename-sorted order for determinism
    results_sorted = sorted(results, key=lambda r: r['name'])
    total_time = sum(r['duration'] for r in results_sorted)

    with LOG_FILE.open('a', encoding='utf-8') as out:
        out.write(f'=== test run start: {time.ctime()}\n')
        out.write(f'Using interpreter: {VENV_PY}\n')
        for r in results_sorted:
            out.write(f"--- {r['name']} (t={r['duration']}s) ---\n")
            out.write(r['stdout'] or '')
            out.write(r['stderr'] or '')
            out.write(f"EXIT CODE: {r['rc']}\n")
        out.write(f'TOTAL TIME: {round(total_time,3)}s\n')
        out.write('=== test run end\n\n')

    # Append environment info to README.md (absolute path + python/pip versions)
    py_ver = subprocess.run([str(VENV_PY), '--version'], capture_output=True, text=True).stdout.strip()
    pip_ver = subprocess.run([str(VENV_PY), '-m', 'pip', '--version'], capture_output=True, text=True).stdout.strip()
    info = f"\nEnvironment: .venv\nAbsolute path: {ROOT / '.venv'}\n{py_ver} | {pip_ver}\n"
    with README.open('a', encoding='utf-8') as r:
        r.write('\n' + '---\n' + info)

    # Return non-zero if any test failed
    failed = [r for r in results_sorted if r['rc'] != 0]
    if failed:
        print(f"{len(failed)} test(s) failed — see {LOG_FILE}")
        return 1

    print(f"All tests passed in {round(total_time,3)}s — details in {LOG_FILE}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
