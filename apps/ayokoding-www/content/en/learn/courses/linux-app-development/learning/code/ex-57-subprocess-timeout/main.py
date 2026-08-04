"""Handle a child process that exceeds its time budget."""

import subprocess

try:
    subprocess.run(["sh", "-c", "sleep 1"], timeout=0.01, check=True)
except subprocess.TimeoutExpired:
    print("notes: child timed out")
