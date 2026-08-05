"""Capture a child process's stdout as text."""

import subprocess

result = subprocess.run(
    ["printf", "notes-daemon\n"], capture_output=True, check=True, text=True
)
print(result.stdout.strip())
