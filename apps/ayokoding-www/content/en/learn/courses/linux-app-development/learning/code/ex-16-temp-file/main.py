"""Create and remove an isolated temporary file."""

import tempfile
from pathlib import Path

with tempfile.NamedTemporaryFile(
    prefix="notes-", suffix=".txt", delete=False
) as handle:
    path = Path(handle.name)
    handle.write(b"draft")
try:
    print(path.read_text(encoding="utf-8"))
finally:
    path.unlink(missing_ok=True)
