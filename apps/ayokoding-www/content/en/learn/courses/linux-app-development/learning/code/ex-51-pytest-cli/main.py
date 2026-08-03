"""Test a CLI process boundary with pytest."""

import subprocess
import sys


def test_cli_prints_status():
    result = subprocess.run(
        [sys.executable, "-c", "print('pending=2')"],
        capture_output=True,
        check=True,
        text=True,
    )
    assert result.stdout == "pending=2\n"
