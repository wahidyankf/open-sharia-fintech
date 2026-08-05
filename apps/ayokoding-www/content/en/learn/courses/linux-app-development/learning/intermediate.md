---
title: "Intermediate Examples"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 20
---

Examples 27–54 cover failures, pipes, signals, daemon lifecycle, service units, scheduling, packaging, sockets, and tests.

### Example 27: subprocess check

_ex-27 · exercises the matching syllabus concept_

**`learning/code/ex-27-subprocess-check/main.py`**

```python
"""Turn a failed child process into an explicit result."""
import subprocess

try:
    subprocess.run(["sh", "-c", "exit 4"], check=True)
except subprocess.CalledProcessError as error:
    print(f"child failed with {error.returncode}")

```

**Run**: `python3 main.py` from the example directory.

### Example 28: subprocess returncode

_ex-28 · exercises the matching syllabus concept_

**`learning/code/ex-28-subprocess-returncode/main.py`**

```python
"""Inspect a child process return code without raising."""
import subprocess

result = subprocess.run(["sh", "-c", "exit 4"], check=False)
print(result.returncode)

```

**Run**: `python3 main.py` from the example directory.

### Example 29: subprocess stderr

_ex-29 · exercises the matching syllabus concept_

**`learning/code/ex-29-subprocess-stderr/main.py`**

```python
"""Capture a child's diagnostic stream."""
import subprocess

result = subprocess.run(
    ["sh", "-c", "printf 'bad note\\n' >&2; exit 2"],
    capture_output=True,
    check=False,
    text=True,
)
print(result.stderr.strip(), result.returncode)

```

**Run**: `python3 main.py` from the example directory.

### Example 30: pipe processes

_ex-30 · exercises the matching syllabus concept_

**`learning/code/ex-30-pipe-processes/main.py`**

```python
"""Connect one child process's stdout to another's stdin."""
import subprocess

producer = subprocess.Popen(["printf", "note\\n"], stdout=subprocess.PIPE, text=True)
assert producer.stdout is not None
consumer = subprocess.run(
    ["tr", "a-z", "A-Z"], stdin=producer.stdout, capture_output=True, check=True, text=True
)
producer.stdout.close()
producer.wait()
print(consumer.stdout.strip())

```

**Run**: `python3 main.py` from the example directory.

### Example 31: popen stdin

_ex-31 · exercises the matching syllabus concept_

**`learning/code/ex-31-popen-stdin/main.py`**

```python
"""Send application data to a running child process."""
import subprocess

child = subprocess.Popen(
    ["tr", "a-z", "A-Z"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True
)
stdout, _ = child.communicate("notes\\n")
print(stdout.strip(), child.returncode)

```

**Run**: `python3 main.py` from the example directory.

### Example 32: signal sigint

_ex-32 · exercises the matching syllabus concept_

**`learning/code/ex-32-signal-sigint/main.py`**

```python
"""Handle the actual SIGINT signal as a cooperative stop request."""
import signal

stopped = False


def request_stop(number, _frame):
    global stopped
    assert number == signal.SIGINT
    stopped = True


signal.signal(signal.SIGINT, request_stop)
signal.raise_signal(signal.SIGINT)
print("stopped" if stopped else "running")

```

**Run**: `python3 main.py` from the example directory.

### Example 33: signal sigterm

_ex-33 · exercises the matching syllabus concept_

**`learning/code/ex-33-signal-sigterm/main.py`**

```python
"""Handle the actual SIGTERM signal used by service managers."""
import signal

stopped = False


def request_stop(number, _frame):
    global stopped
    assert number == signal.SIGTERM
    stopped = True


signal.signal(signal.SIGTERM, request_stop)
signal.raise_signal(signal.SIGTERM)
print("stopped" if stopped else "running")

```

**Run**: `python3 main.py` from the example directory.

### Example 34: graceful flag

_ex-34 · exercises the matching syllabus concept_

**`learning/code/ex-34-graceful-flag/main.py`**

```python
"""Let the signal handler set a flag that the work loop observes."""
import signal

running = True
processed = []


def request_stop(_number, _frame):
    global running
    running = False


signal.signal(signal.SIGTERM, request_stop)
while running and len(processed) < 1:
    processed.append("one note")
    signal.raise_signal(signal.SIGTERM)
print(processed, running)

```

**Run**: `python3 main.py` from the example directory.

### Example 35: cleanup on signal

_ex-35 · exercises the matching syllabus concept_

**`learning/code/ex-35-cleanup-on-signal/main.py`**

```python
"""Perform cleanup after, rather than inside, the signal handler."""
import signal
import tempfile
from pathlib import Path

running = True


def request_stop(_number, _frame):
    global running
    running = False


with tempfile.TemporaryDirectory() as directory:
    socket_marker = Path(directory) / "notes.sock"
    socket_marker.touch()
    signal.signal(signal.SIGTERM, request_stop)
    signal.raise_signal(signal.SIGTERM)
    if not running:
        socket_marker.unlink()
    print(not socket_marker.exists())

```

**Run**: `python3 main.py` from the example directory.

### Example 36: daemon loop

_ex-36 · exercises the matching syllabus concept_

**`learning/code/ex-36-daemon-loop/main.py`**

```python
"""Model a bounded daemon work loop."""
import time

running = True
for cycle in range(2):
    if not running:
        break
    print(f"polling cycle {cycle}")
    time.sleep(0.01)
print("daemon loop ended")

```

**Run**: `python3 main.py` from the example directory.

### Example 37: daemon log

_ex-37 · exercises the matching syllabus concept_

**`learning/code/ex-37-daemon-log/main.py`**

```python
"""Log daemon lifecycle events instead of printing them."""
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")
logging.info("notes daemon started")
logging.info("notes daemon stopped")

```

**Run**: `python3 main.py` from the example directory.

### Example 38: daemon signal stop

_ex-38 · exercises the matching syllabus concept_

**`learning/code/ex-38-daemon-signal-stop/main.py`**

```python
"""Combine a service loop with SIGTERM shutdown."""
import signal
import time

running = True


def stop(_number, _frame):
    global running
    running = False


signal.signal(signal.SIGTERM, stop)
for cycle in range(2):
    print(f"cycle {cycle}")
    if cycle == 0:
        signal.raise_signal(signal.SIGTERM)
    if not running:
        break
    time.sleep(0.01)
print("stopped cleanly")

```

**Run**: `python3 main.py` from the example directory.

### Example 39: systemd unit

_ex-39 · exercises the matching syllabus concept_

**`learning/code/ex-39-systemd-unit/main.py`**

```python
"""Generate the essential directives of a systemd service unit."""
unit = """[Service]
Type=simple
ExecStart=/usr/bin/notes-linux-daemon
Restart=on-failure
"""
print(unit)

```

**Run**: `python3 main.py` from the example directory.

### Example 40: systemd lifecycle

_ex-40 · exercises the matching syllabus concept_

**`learning/code/ex-40-systemd-lifecycle/main.py`**

```python
"""Describe the systemd actions that manage a changed service."""
commands = [
    "systemctl daemon-reload",
    "systemctl enable --now notes-linux.service",
    "systemctl status notes-linux.service",
]
print("\n".join(commands))

```

**Run**: `python3 main.py` from the example directory.

### Example 41: cron entry

_ex-41 · exercises the matching syllabus concept_

**`learning/code/ex-41-cron-entry/main.py`**

```python
"""Construct a cron schedule for periodic, finite work."""
minute = "*/15"
command = "/usr/local/bin/notes-linux --compact"
print(f"{minute} * * * * {command}")

```

**Run**: `python3 main.py` from the example directory.

### Example 42: pyproject min

_ex-42 · exercises the matching syllabus concept_

**`learning/code/ex-42-pyproject-min/main.py`**

```python
"""Show a minimal valid pyproject project table."""
import tomllib

pyproject = """[project]
name = "notes-linux"
version = "0.1.0"
"""
project = tomllib.loads(pyproject)["project"]
print(project["name"], project["version"])

```

**Run**: `python3 main.py` from the example directory.

### Example 43: pyproject metadata

_ex-43 · exercises the matching syllabus concept_

**`learning/code/ex-43-pyproject-metadata/main.py`**

```python
"""Read useful package metadata from a pyproject document."""
import tomllib

pyproject = """[project]
name = "notes-linux"
version = "0.1.0"
description = "Local notes service"
requires-python = ">=3.11"
"""
project = tomllib.loads(pyproject)["project"]
print(project["description"], project["requires-python"])

```

**Run**: `python3 main.py` from the example directory.

### Example 44: declare dependency

_ex-44 · exercises the matching syllabus concept_

**`learning/code/ex-44-declare-dependency/main.py`**

```python
"""Declare and inspect an actual runtime dependency in pyproject syntax."""
import tomllib

pyproject = """[project]
name = "notes-linux"
version = "0.1.0"
dependencies = ["platformdirs>=4.2"]
"""
dependencies = tomllib.loads(pyproject)["project"]["dependencies"]
assert dependencies == ["platformdirs>=4.2"]
print(dependencies[0])

```

**Run**: `python3 main.py` from the example directory.

### Example 45: install editable

_ex-45 · exercises the matching syllabus concept_

**`learning/code/ex-45-install-editable/main.py`**

```python
"""Show the command that installs the current project in editable mode."""
import sys

print(f"{sys.executable} -m pip install -e .")

```

**Run**: `python3 main.py` from the example directory.

### Example 46: console script

_ex-46 · exercises the matching syllabus concept_

**`learning/code/ex-46-console-script/main.py`**

```python
"""Declare a console script entry point."""
import tomllib

pyproject = """[project]
name = "notes-linux"
version = "0.1.0"

[project.scripts]
notes-linux = "notes_linux.cli:main"
"""
print(tomllib.loads(pyproject)["project"]["scripts"]["notes-linux"])

```

**Run**: `python3 main.py` from the example directory.

### Example 47: entry point invoke

_ex-47 · exercises the matching syllabus concept_

**`learning/code/ex-47-entry-point-invoke/main.py`**

```python
"""Invoke the callable used by a console-script entry point."""

def main(argv: list[str]) -> int:
    print(f"notes command: {argv[0]}")
    return 0


assert main(["status"]) == 0

```

**Run**: `python3 main.py` from the example directory.

### Example 48: config plus logging

_ex-48 · exercises the matching syllabus concept_

**`learning/code/ex-48-config-plus-logging/main.py`**

```python
"""Load configuration before configuring a logger."""
import configparser
import logging

config = configparser.ConfigParser()
config.read_dict({"logging": {"level": "INFO"}})
logging.basicConfig(
    level=getattr(logging, config["logging"]["level"]), format="%(levelname)s:%(message)s"
)
logging.info("configured notes daemon")

```

**Run**: `python3 main.py` from the example directory.

### Example 49: unix socket

_ex-49 · exercises the matching syllabus concept_

**`learning/code/ex-49-unix-socket/main.py`**

```python
"""Exchange a real request and reply over a Unix-domain socket."""
import socket
import tempfile
import threading
from pathlib import Path

with tempfile.TemporaryDirectory() as directory:
    path = Path(directory) / "notes.sock"
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as server:
        server.bind(str(path))
        server.listen(1)

        def reply():
            connection, _ = server.accept()
            with connection:
                assert connection.recv(16) == b"STATUS"
                connection.sendall(b"OK")

        worker = threading.Thread(target=reply)
        worker.start()
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
            client.connect(str(path))
            client.sendall(b"STATUS")
            print(client.recv(16).decode())
        worker.join()

```

**Run**: `python3 main.py` from the example directory.

### Example 50: tcp socket

_ex-50 · exercises the matching syllabus concept_

**`learning/code/ex-50-tcp-socket/main.py`**

```python
"""Exchange a real request and reply over localhost TCP."""
import socket
import threading

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind(("127.0.0.1", 0))
    server.listen(1)
    host, port = server.getsockname()

    def reply():
        connection, _ = server.accept()
        with connection:
            assert connection.recv(16) == b"PING"
            connection.sendall(b"PONG")

    worker = threading.Thread(target=reply)
    worker.start()
    with socket.create_connection((host, port)) as client:
        client.sendall(b"PING")
        print(client.recv(16).decode())
    worker.join()

```

**Run**: `python3 main.py` from the example directory.

### Example 51: pytest cli

_ex-51 · exercises the matching syllabus concept_

**`learning/code/ex-51-pytest-cli/main.py`**

```python
"""Test a CLI process boundary with pytest."""
import subprocess
import sys


def test_cli_prints_status():
    result = subprocess.run(
        [sys.executable, "-c", "print('pending=2')"], capture_output=True, check=True, text=True
    )
    assert result.stdout == "pending=2\n"

```

**Run**: `pytest main.py` from the example directory.

### Example 52: pytest capsys

_ex-52 · exercises the matching syllabus concept_

**`learning/code/ex-52-pytest-capsys/main.py`**

```python
"""Test stdout and stderr separately with pytest capsys."""
import sys


def emit_status():
    print("pending=2")
    print("notes: diagnostic", file=sys.stderr)


def test_streams_are_separate(capsys):
    emit_status()
    captured = capsys.readouterr()
    assert captured.out == "pending=2\n"
    assert captured.err == "notes: diagnostic\n"

```

**Run**: `pytest main.py` from the example directory.

### Example 53: mock subprocess

_ex-53 · exercises the matching syllabus concept_

**`learning/code/ex-53-mock-subprocess/main.py`**

```python
"""Mock a child-process boundary without launching a process."""
import subprocess
from unittest.mock import patch


def current_branch() -> str:
    return subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True).stdout


def test_current_branch():
    completed = subprocess.CompletedProcess(["git"], 0, stdout="main\n")
    with patch("subprocess.run", return_value=completed) as run:
        assert current_branch() == "main\n"
    run.assert_called_once()

```

**Run**: `pytest main.py` from the example directory.

### Example 54: test exit code

_ex-54 · exercises the matching syllabus concept_

**`learning/code/ex-54-test-exit-code/main.py`**

```python
"""Assert a CLI's documented non-zero invalid-input contract."""
import subprocess
import sys


def test_invalid_input_exits_two():
    result = subprocess.run(
        [sys.executable, "-c", "import sys; print('bad input', file=sys.stderr); raise SystemExit(2)"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2
    assert result.stderr == "bad input\n"

```

**Run**: `pytest main.py` from the example directory.
