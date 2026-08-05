"""Write a UTF-8 note to a file."""

import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as directory:
    note = Path(directory) / "today.txt"
    note.write_text("ship the daemon\n", encoding="utf-8")
    print(note.exists(), note.stat().st_size)
