"""Create a clean environment before installing a package."""

import tempfile
import venv
from pathlib import Path

with tempfile.TemporaryDirectory() as directory:
    root = Path(directory)
    venv.EnvBuilder(with_pip=False).create(root / "clean")
    print((root / "clean" / "pyvenv.cfg").read_text(encoding="utf-8").splitlines()[0])
