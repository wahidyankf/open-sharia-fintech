"""Capstone Step 2: verifies shell.py end to end, as a REAL subprocess CLI invocation.

Runs `python3 shell.py <file>` exactly the way a user would from a terminal, and checks the
captured stdout/exit code -- the strongest form of "runs end to end from the CLI" this capstone
can demonstrate, stronger than calling main() in-process.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

CODE_DIR = Path(__file__).parent
SHELL_PATH = CODE_DIR / "shell.py"
SAMPLE_CSV = CODE_DIR / "sample_transactions.csv"
BAD_CSV = CODE_DIR / "bad_transactions.csv"


def run_shell(
    *args: str,
) -> subprocess.CompletedProcess[str]:  # => the ONE helper every test below reuses
    return subprocess.run(  # => a REAL child process, exactly like a user typing this at a terminal
        [sys.executable, str(SHELL_PATH), *args],
        capture_output=True,
        text=True,
        check=False,  # => this suite inspects returncode itself -- a non-zero exit is a valid case, not a crash
    )


def test_shell_on_valid_csv_prints_the_report_and_exits_zero() -> None:
    completed = run_shell(str(SAMPLE_CSV))
    assert completed.returncode == 0
    assert "electronics: 288.99" in completed.stdout
    assert "groceries: 58.25" in completed.stdout
    assert "books: 15.25" in completed.stdout
    assert "apparel: 60.00" in completed.stdout
    assert "Top category: electronics" in completed.stdout


def test_shell_on_malformed_csv_reports_errors_and_exits_nonzero_without_crashing() -> (
    None
):
    completed = run_shell(str(BAD_CSV))
    assert (
        completed.returncode == 1
    )  # => a controlled non-zero exit -- NOT a Python traceback
    assert "4 error(s) found" in completed.stdout
    assert (
        "Traceback" not in completed.stderr
    )  # => co-23: proves the shell never let an exception escape


def test_shell_with_no_arguments_prints_usage_and_exits_two() -> None:
    completed = run_shell()
    assert completed.returncode == 2
    assert "usage: shell.py" in completed.stderr


# => Run: pytest -q -- Output: 3 passed
