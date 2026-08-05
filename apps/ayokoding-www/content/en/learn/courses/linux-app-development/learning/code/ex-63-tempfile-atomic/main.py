"""Atomically replace a note with a temporary sibling file."""

import os
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as directory:
    target = Path(directory) / "note.txt"
    target.write_text("old", encoding="utf-8")
    descriptor, temporary_name = tempfile.mkstemp(dir=directory, prefix=".note-")
    with os.fdopen(descriptor, "w", encoding="utf-8") as temporary:
        temporary.write("new")
    os.replace(temporary_name, target)
    print(target.read_text(encoding="utf-8"))
