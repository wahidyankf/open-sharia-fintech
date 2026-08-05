"""Create an isolated Python virtual environment."""

import tempfile
import venv
from pathlib import Path

with tempfile.TemporaryDirectory() as directory:
    environment = Path(directory) / "venv"
    venv.EnvBuilder(with_pip=False).create(environment)
    print((environment / "pyvenv.cfg").is_file())
