"""Compose a Linux path with pathlib."""

from pathlib import Path

config = Path.home() / ".config" / "notes-linux" / "config.ini"
print(config)
