"""Inspect a child process return code without raising."""

import subprocess

result = subprocess.run(["sh", "-c", "exit 4"], check=False)
print(result.returncode)
