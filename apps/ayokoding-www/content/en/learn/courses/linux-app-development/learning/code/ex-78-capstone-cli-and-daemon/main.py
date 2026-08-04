"""Run the actual capstone CLI and daemon as separate Linux processes."""

import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

CAPSTONE = Path(__file__).parents[3] / "capstone" / "code"
sys.path.insert(0, str(CAPSTONE))

from notes_linux import cli  # noqa: E402


with tempfile.TemporaryDirectory() as directory:
    path = Path(directory) / "n.sock"
    environment = {**os.environ, "PYTHONPATH": str(CAPSTONE)}
    daemon = subprocess.Popen(
        [sys.executable, "-m", "notes_linux.daemon", "--socket", str(path)],
        env=environment,
    )
    try:
        deadline = time.monotonic() + 2
        while not path.exists() and time.monotonic() < deadline:
            time.sleep(0.01)
        assert path.exists()
        assert cli.main(["status", "--socket", str(path)]) == 0
    finally:
        daemon.terminate()
        daemon.wait(timeout=2)
print("notes-linux CLI reached its daemon")
