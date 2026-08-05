---
title: "Beginner Examples"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 10
---

Examples 1–26 establish Linux process behavior: arguments, exit codes, streams, environment, files, logging, configuration, subprocesses, venv, and pytest.

### Example 1: sys argv

_ex-01 · exercises the matching syllabus concept_

**`learning/code/ex-01-sys-argv/main.py`**

```python
"""Print the positional arguments a Linux process receives."""
import sys

print(sys.argv[1:])

```

**Run**: `python3 main.py` from the example directory.

### Example 2: argparse basic

_ex-02 · exercises the matching syllabus concept_

**`learning/code/ex-02-argparse-basic/main.py`**

```python
"""Parse one required argument."""
import argparse

parser = argparse.ArgumentParser(prog="notes")
parser.add_argument("title")
print(parser.parse_args(["standup"]).title)

```

**Run**: `python3 main.py` from the example directory.

### Example 3: argparse help

_ex-03 · exercises the matching syllabus concept_

**`learning/code/ex-03-argparse-help/main.py`**

```python
"""Expose argparse's real --help contract."""
import argparse

parser = argparse.ArgumentParser(prog="notes-linux", description="Read a local note")
parser.add_argument("note", nargs="?")
try:
    parser.parse_args(["--help"])
except SystemExit as error:
    assert error.code == 0

```

**Run**: `python3 main.py` from the example directory.

### Example 4: argparse optional

_ex-04 · exercises the matching syllabus concept_

**`learning/code/ex-04-argparse-optional/main.py`**

```python
"""Parse an optional flag with a useful default."""
import argparse

parser = argparse.ArgumentParser(prog="notes")
parser.add_argument("--format", choices=["text", "json"], default="text")
print(parser.parse_args(["--format", "json"]).format)

```

**Run**: `python3 main.py` from the example directory.

### Example 5: argparse subcommand

_ex-05 · exercises the matching syllabus concept_

**`learning/code/ex-05-argparse-subcommand/main.py`**

```python
"""Dispatch an argparse subcommand."""
import argparse

parser = argparse.ArgumentParser(prog="notes")
commands = parser.add_subparsers(dest="command", required=True)
commands.add_parser("status")
print(parser.parse_args(["status"]).command)

```

**Run**: `python3 main.py` from the example directory.

### Example 6: exit zero

_ex-06 · exercises the matching syllabus concept_

**`learning/code/ex-06-exit-zero/main.py`**

```python
"""Finish a successful command with status zero."""
import sys

print("note saved")
raise SystemExit(0)

```

**Run**: `python3 main.py` from the example directory.

### Example 7: exit nonzero

_ex-07 · exercises the matching syllabus concept_

**`learning/code/ex-07-exit-nonzero/main.py`**

```python
"""Report invalid input and use a non-zero process status."""
import sys

print("notes: title must not be empty", file=sys.stderr)
raise SystemExit(2)

```

**Run**: `python3 main.py` from the example directory.

### Example 8: stderr write

_ex-08 · exercises the matching syllabus concept_

**`learning/code/ex-08-stderr-write/main.py`**

```python
"""Write a diagnostic to the stderr stream."""
import sys

sys.stderr.write("notes: configuration is missing\n")

```

**Run**: `python3 main.py` from the example directory.

### Example 9: stdout vs stderr

_ex-09 · exercises the matching syllabus concept_

**`learning/code/ex-09-stdout-vs-stderr/main.py`**

```python
"""Keep machine-readable output separate from diagnostics."""
import sys

print("pending=2")
print("notes: status served locally", file=sys.stderr)

```

**Run**: `python3 main.py` from the example directory.

### Example 10: read env

_ex-10 · exercises the matching syllabus concept_

**`learning/code/ex-10-read-env/main.py`**

```python
"""Read a process environment variable."""
import os

print(os.environ["NOTES_MODE"] if "NOTES_MODE" in os.environ else "unset")

```

**Run**: `python3 main.py` from the example directory.

### Example 11: env default

_ex-11 · exercises the matching syllabus concept_

**`learning/code/ex-11-env-default/main.py`**

```python
"""Use a safe environment fallback."""
import os

print(os.environ.get("NOTES_MODE", "development"))

```

**Run**: `python3 main.py` from the example directory.

### Example 12: read file

_ex-12 · exercises the matching syllabus concept_

**`learning/code/ex-12-read-file/main.py`**

```python
"""Read a UTF-8 note from a file."""
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as directory:
    note = Path(directory) / "today.txt"
    note.write_text("ship the daemon\n", encoding="utf-8")
    print(note.read_text(encoding="utf-8").strip())

```

**Run**: `python3 main.py` from the example directory.

### Example 13: write file

_ex-13 · exercises the matching syllabus concept_

**`learning/code/ex-13-write-file/main.py`**

```python
"""Write a UTF-8 note to a file."""
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as directory:
    note = Path(directory) / "today.txt"
    note.write_text("ship the daemon\n", encoding="utf-8")
    print(note.exists(), note.stat().st_size)

```

**Run**: `python3 main.py` from the example directory.

### Example 14: pathlib

_ex-14 · exercises the matching syllabus concept_

**`learning/code/ex-14-pathlib/main.py`**

```python
"""Compose a Linux path with pathlib."""
from pathlib import Path

config = Path.home() / ".config" / "notes-linux" / "config.ini"
print(config)

```

**Run**: `python3 main.py` from the example directory.

### Example 15: file mode

_ex-15 · exercises the matching syllabus concept_

**`learning/code/ex-15-file-mode/main.py`**

```python
"""Restrict a private file to its owner."""
import os
import stat
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as directory:
    path = Path(directory) / "token"
    path.write_text("private", encoding="utf-8")
    os.chmod(path, 0o600)
    print(oct(stat.S_IMODE(path.stat().st_mode)))

```

**Run**: `python3 main.py` from the example directory.

### Example 16: temp file

_ex-16 · exercises the matching syllabus concept_

**`learning/code/ex-16-temp-file/main.py`**

```python
"""Create and remove an isolated temporary file."""
import tempfile
from pathlib import Path

with tempfile.NamedTemporaryFile(prefix="notes-", suffix=".txt", delete=False) as handle:
    path = Path(handle.name)
    handle.write(b"draft")
try:
    print(path.read_text(encoding="utf-8"))
finally:
    path.unlink(missing_ok=True)

```

**Run**: `python3 main.py` from the example directory.

### Example 17: logging basic

_ex-17 · exercises the matching syllabus concept_

**`learning/code/ex-17-logging-basic/main.py`**

```python
"""Emit one INFO record through Python logging."""
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")
logging.info("notes daemon started")

```

**Run**: `python3 main.py` from the example directory.

### Example 18: logging levels

_ex-18 · exercises the matching syllabus concept_

**`learning/code/ex-18-logging-levels/main.py`**

```python
"""Use logging levels to separate normal and verbose events."""
import logging

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(message)s")
logging.debug("socket path resolved")
logging.info("daemon ready")
logging.warning("retrying connection")

```

**Run**: `python3 main.py` from the example directory.

### Example 19: config file

_ex-19 · exercises the matching syllabus concept_

**`learning/code/ex-19-config-file/main.py`**

```python
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

```

**Run**: `python3 main.py` from the example directory.

### Example 20: xdg config

_ex-20 · exercises the matching syllabus concept_

**`learning/code/ex-20-xdg-config/main.py`**

```python
"""Resolve configuration according to XDG_CONFIG_HOME."""
import os
from pathlib import Path

root = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
print(root / "notes-linux" / "config.ini")

```

**Run**: `python3 main.py` from the example directory.

### Example 21: fd stdin

_ex-21 · exercises the matching syllabus concept_

**`learning/code/ex-21-fd-stdin/main.py`**

```python
"""Consume data delivered through standard input."""
import io
import sys

original = sys.stdin
try:
    sys.stdin = io.StringIO("first note\n")
    print(sys.stdin.read().strip())
finally:
    sys.stdin = original

```

**Run**: `python3 main.py` from the example directory.

### Example 22: fd redirect

_ex-22 · exercises the matching syllabus concept_

**`learning/code/ex-22-fd-redirect/main.py`**

```python
"""Redirect stdout to a file descriptor-backed stream."""
import contextlib
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as directory:
    path = Path(directory) / "status.txt"
    with path.open("w", encoding="utf-8") as output:
        with contextlib.redirect_stdout(output):
            print("pending=2")
    print(path.read_text(encoding="utf-8").strip())

```

**Run**: `python3 main.py` from the example directory.

### Example 23: subprocess run

_ex-23 · exercises the matching syllabus concept_

**`learning/code/ex-23-subprocess-run/main.py`**

```python
"""Run a child process and require success."""
import subprocess

subprocess.run(["printf", "notes-daemon\n"], check=True)

```

**Run**: `python3 main.py` from the example directory.

### Example 24: subprocess output

_ex-24 · exercises the matching syllabus concept_

**`learning/code/ex-24-subprocess-output/main.py`**

```python
"""Capture a child process's stdout as text."""
import subprocess

result = subprocess.run(
    ["printf", "notes-daemon\n"], capture_output=True, check=True, text=True
)
print(result.stdout.strip())

```

**Run**: `python3 main.py` from the example directory.

### Example 25: venv create

_ex-25 · exercises the matching syllabus concept_

**`learning/code/ex-25-venv-create/main.py`**

```python
"""Create an isolated Python virtual environment."""
import tempfile
import venv
from pathlib import Path

with tempfile.TemporaryDirectory() as directory:
    environment = Path(directory) / "venv"
    venv.EnvBuilder(with_pip=False).create(environment)
    print((environment / "pyvenv.cfg").is_file())

```

**Run**: `python3 main.py` from the example directory.

### Example 26: pytest first

_ex-26 · exercises the matching syllabus concept_

**`learning/code/ex-26-pytest-first/main.py`**

```python
"""A first pytest test for Linux application core logic."""

def status_line(count: int) -> str:
    return f"pending={count}"


def test_status_line():
    assert status_line(2) == "pending=2"

```

**Run**: `pytest main.py` from the example directory.
