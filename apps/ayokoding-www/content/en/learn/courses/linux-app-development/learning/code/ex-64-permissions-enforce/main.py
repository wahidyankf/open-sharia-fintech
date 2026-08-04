"""Reject a private configuration file with unsafe permissions."""

import os
import stat
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as directory:
    path = Path(directory) / "config.ini"
    path.write_text("[notes]", encoding="utf-8")
    os.chmod(path, 0o644)
    mode = stat.S_IMODE(path.stat().st_mode)
    if mode & 0o077:
        print(f"refusing unsafe mode {oct(mode)}")
