"""Test an error return from a failing child process."""

import subprocess


def test_child_failure_has_stderr():
    result = subprocess.run(
        ["sh", "-c", "printf broken >&2; exit 7"], capture_output=True, text=True
    )
    assert result.returncode == 7
    assert result.stderr == "broken"
