"""Mock a child-process boundary without launching a process."""

import subprocess
from unittest.mock import patch


def current_branch() -> str:
    return subprocess.run(
        ["git", "branch", "--show-current"], capture_output=True, text=True
    ).stdout


def test_current_branch():
    completed = subprocess.CompletedProcess(["git"], 0, stdout="main\n")
    with patch("subprocess.run", return_value=completed) as run:
        assert current_branch() == "main\n"
    run.assert_called_once()
