"""Redirect stdout to a file descriptor-backed stream."""

import contextlib
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as directory:
    path = Path(directory) / "status.txt"
    with path.open("w", encoding="utf-8") as output:
        with contextlib.redirect_stdout(output):
            print("pending=2")
    print(path.read_text(encoding="utf-8").strip())
