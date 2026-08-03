"""Turn a failed child process into an explicit result."""

import subprocess

try:
    subprocess.run(["sh", "-c", "exit 4"], check=True)
except subprocess.CalledProcessError as error:
    print(f"child failed with {error.returncode}")
