"""Read a UTF-8 note from a file."""

import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as directory:
    note = Path(directory) / "today.txt"
    note.write_text("ship the daemon\n", encoding="utf-8")
    print(note.read_text(encoding="utf-8").strip())
