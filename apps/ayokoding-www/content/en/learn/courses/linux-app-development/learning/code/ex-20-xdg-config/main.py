"""Resolve configuration according to XDG_CONFIG_HOME."""

import os
from pathlib import Path

root = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
print(root / "notes-linux" / "config.ini")
