"""Restrict a private file to its owner."""

import os
import stat
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as directory:
    path = Path(directory) / "token"
    path.write_text("private", encoding="utf-8")
    os.chmod(path, 0o600)
    print(oct(stat.S_IMODE(path.stat().st_mode)))
