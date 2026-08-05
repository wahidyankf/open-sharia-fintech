"""Load an INI configuration file."""

import configparser
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as directory:
    path = Path(directory) / "config.ini"
    path.write_text("[daemon]\ninterval = 5\n", encoding="utf-8")
    config = configparser.ConfigParser()
    config.read(path, encoding="utf-8")
    print(config.getint("daemon", "interval"))
