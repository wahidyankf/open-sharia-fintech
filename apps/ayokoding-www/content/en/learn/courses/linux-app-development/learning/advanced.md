---
title: "Advanced Examples"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 30
---

Examples 55–78 combine the earlier boundaries into resilient CLIs and services. GTK, Qt, and container entries are optional surveys; no toolkit or Docker version is assumed.

### Example 55: Full Cli

_ex-55 · `full-cli` · exercises co-03, co-07, co-08, co-04_

**`learning/code/ex-55-full-cli/main.py`**

```python
"""Implement a complete small CLI with an explicit success contract."""
import argparse


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="notes")
    parser.add_argument("command", choices=["status"])
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args(argv)
    print('{"pending": 2}' if args.format == "json" else "pending=2")
    return 0


raise SystemExit(main(["status"]))

```

**Run**: `python3 main.py` from this example directory.

**Key takeaway**: Keep full cli explicit and observable at the Linux application boundary.

---

### Example 56: Cli Bad Input

_ex-56 · `cli-bad-input` · exercises co-04, co-05, co-01_

**`learning/code/ex-56-cli-bad-input/main.py`**

```python
"""Make invalid CLI input a stable stderr-and-exit-code contract."""
import argparse
import sys


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="notes", add_help=False)
    parser.add_argument("command", choices=["status"])
    try:
        parser.parse_args(argv)
    except SystemExit:
        print("notes: command must be status", file=sys.stderr)
        return 2
    print("pending=2")
    return 0


assert main(["unknown"]) == 2

```

**Run**: `python3 main.py` from this example directory.

**Key takeaway**: Keep cli bad input explicit and observable at the Linux application boundary.

---

### Example 57: Subprocess Timeout

_ex-57 · `subprocess-timeout` · exercises co-14_

**`learning/code/ex-57-subprocess-timeout/main.py`**

```python
"""Handle a child process that exceeds its time budget."""
import subprocess

try:
    subprocess.run(["sh", "-c", "sleep 1"], timeout=0.01, check=True)
except subprocess.TimeoutExpired:
    print("notes: child timed out")

```

**Run**: `python3 main.py` from this example directory.

**Key takeaway**: Keep subprocess timeout explicit and observable at the Linux application boundary.

---

### Example 58: Pipe Error Handling

_ex-58 · `pipe-error-handling` · exercises co-15, co-14_

**`learning/code/ex-58-pipe-error-handling/main.py`**

```python
"""Surface a failed producer in a Unix pipeline."""
import subprocess

producer = subprocess.Popen(["sh", "-c", "printf partial; exit 3"], stdout=subprocess.PIPE)
assert producer.stdout is not None
consumer = subprocess.run(["cat"], stdin=producer.stdout, capture_output=True, check=True)
producer.stdout.close()
returncode = producer.wait()
print(consumer.stdout.decode(), returncode)

```

**Run**: `python3 main.py` from this example directory.

**Key takeaway**: Keep pipe error handling explicit and observable at the Linux application boundary.

---

### Example 59: Daemon Systemd

_ex-59 · `daemon-systemd` · exercises co-18, co-19, co-17_

**`learning/code/ex-59-daemon-systemd/main.py`**

```python
"""Pair a daemon command with systemd's restart policy."""
unit = """[Unit]
Description=Notes daemon

[Service]
ExecStart=/usr/bin/python3 -m notes_linux.daemon
Restart=on-failure
"""
assert "Restart=on-failure" in unit
print(unit)

```

**Run**: `python3 main.py` from this example directory.

**Key takeaway**: Keep daemon systemd explicit and observable at the Linux application boundary.

---

### Example 60: Daemon Restart

_ex-60 · `daemon-restart` · exercises co-19_

**`learning/code/ex-60-daemon-restart/main.py`**

```python
"""Explain restart behavior for failures but not clean exits."""
exit_statuses = {"clean shutdown": 0, "uncaught failure": 1}
for event, status in exit_statuses.items():
    print(event, "restart" if status != 0 else "do not restart")

```

**Run**: `python3 main.py` from this example directory.

**Key takeaway**: Keep daemon restart explicit and observable at the Linux application boundary.

---

### Example 61: Cron Vs Daemon

_ex-61 · `cron-vs-daemon` · exercises co-20, co-18_

**`learning/code/ex-61-cron-vs-daemon/main.py`**

```python
"""Choose cron for scheduled work and a daemon for continuous work."""
workloads = {"daily cleanup": "cron", "socket status API": "daemon"}
for workload, runner in workloads.items():
    print(f"{workload}: {runner}")

```

**Run**: `python3 main.py` from this example directory.

**Key takeaway**: Keep cron vs daemon explicit and observable at the Linux application boundary.

---

### Example 62: Signal During Work

_ex-62 · `signal-during-work` · exercises co-16, co-17_

**`learning/code/ex-62-signal-during-work/main.py`**

```python
"""Finish the current safe operation after SIGTERM arrives."""
import signal

running = True
completed = []


def stop(_number, _frame):
    global running
    running = False


signal.signal(signal.SIGTERM, stop)
completed.append("atomic write")
signal.raise_signal(signal.SIGTERM)
if not running:
    print(f"stopped after {completed[-1]}")

```

**Run**: `python3 main.py` from this example directory.

**Key takeaway**: Keep signal during work explicit and observable at the Linux application boundary.

---

### Example 63: Tempfile Atomic

_ex-63 · `tempfile-atomic` · exercises co-12, co-09_

**`learning/code/ex-63-tempfile-atomic/main.py`**

```python
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

```

**Run**: `python3 main.py` from this example directory.

**Key takeaway**: Keep tempfile atomic explicit and observable at the Linux application boundary.

---

### Example 64: Permissions Enforce

_ex-64 · `permissions-enforce` · exercises co-10_

**`learning/code/ex-64-permissions-enforce/main.py`**

```python
"""Reject a private configuration file with unsafe permissions."""
import os
import stat
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as directory:
    path = Path(directory) / "config.ini"
    path.write_text("[notes]", encoding="utf-8")
    os.chmod(path, 0o644)
    mode = stat.S_IMODE(path.stat().st_mode)
    if mode & 0o077:
        print(f"refusing unsafe mode {oct(mode)}")

```

**Run**: `python3 main.py` from this example directory.

**Key takeaway**: Keep permissions enforce explicit and observable at the Linux application boundary.

---

### Example 65: Socket Ipc Daemon

_ex-65 · `socket-ipc-daemon` · exercises co-25, co-18_

**`learning/code/ex-65-socket-ipc-daemon/main.py`**

```python
"""Serve one IPC request from a Unix-socket daemon."""
import socket
import tempfile
import threading
from pathlib import Path

with tempfile.TemporaryDirectory() as directory:
    path = Path(directory) / "daemon.sock"
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as server:
        server.bind(str(path))
        server.listen(1)

        def serve_one():
            connection, _ = server.accept()
            with connection:
                command = connection.recv(32)
                connection.sendall(b"OK notes-daemon" if command == b"STATUS" else b"ERROR")

        worker = threading.Thread(target=serve_one)
        worker.start()
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
            client.connect(str(path))
            client.sendall(b"STATUS")
            print(client.recv(32).decode())
        worker.join()

```

**Run**: `python3 main.py` from this example directory.

**Key takeaway**: Keep socket ipc daemon explicit and observable at the Linux application boundary.

---

### Example 66: Gui Gtk Survey

_ex-66 · `gui-gtk-survey` · exercises co-26_

**`learning/code/ex-66-gui-gtk-survey/main.py`**

```python
"""Survey GTK availability without making it a core dependency."""
import importlib.util

available = importlib.util.find_spec("gi") is not None
print(f"GTK available: {available}; GTK is suitable for GNOME-native Linux GUIs.")

```

**Run**: `python3 main.py` from this example directory.

**Key takeaway**: Keep gui gtk survey explicit and observable at the Linux application boundary.

---

### Example 67: Gui Qt Survey

_ex-67 · `gui-qt-survey` · exercises co-26_

**`learning/code/ex-67-gui-qt-survey/main.py`**

```python
"""Survey Qt availability without making it a core dependency."""
import importlib.util

available = importlib.util.find_spec("PySide6") is not None
print(f"Qt available: {available}; Qt is suitable for cross-desktop Linux GUIs.")

```

**Run**: `python3 main.py` from this example directory.

**Key takeaway**: Keep gui qt survey explicit and observable at the Linux application boundary.

---

### Example 68: Container Package

_ex-68 · `container-package` · exercises co-27_

**`learning/code/ex-68-container-package/main.py`**

```python
"""Define a container image that packages the CLI."""
dockerfile = """FROM python:3.13-slim
WORKDIR /app
COPY . .
RUN pip install .
ENTRYPOINT ["notes-linux"]
"""
print(dockerfile)

```

**Run**: `python3 main.py` from this example directory.

**Key takeaway**: Keep container package explicit and observable at the Linux application boundary.

---

### Example 69: Container Run

_ex-69 · `container-run` · exercises co-27_

**`learning/code/ex-69-container-run/main.py`**

```python
"""Show a container run command with a mounted Unix-socket directory."""
image = "notes-linux:dev"
command = f"docker run --rm -v /tmp:/tmp {image} status --socket /tmp/notes-linux.sock"
print(command)

```

**Run**: `python3 main.py` from this example directory.

**Key takeaway**: Keep container run explicit and observable at the Linux application boundary.

---

### Example 70: Package Distribute

_ex-70 · `package-distribute` · exercises co-22, co-23_

**`learning/code/ex-70-package-distribute/main.py`**

```python
"""Define build and distribution commands for a Python package."""
import sys

print(f"{sys.executable} -m build")
print(f"{sys.executable} -m twine check dist/*")

```

**Run**: `python3 main.py` from this example directory.

**Key takeaway**: Keep package distribute explicit and observable at the Linux application boundary.

---

### Example 71: Install Clean Venv

_ex-71 · `install-clean-venv` · exercises co-21, co-24_

**`learning/code/ex-71-install-clean-venv/main.py`**

```python
"""Create a clean environment before installing a package."""
import tempfile
import venv
from pathlib import Path

with tempfile.TemporaryDirectory() as directory:
    root = Path(directory)
    venv.EnvBuilder(with_pip=False).create(root / "clean")
    print((root / "clean" / "pyvenv.cfg").read_text(encoding="utf-8").splitlines()[0])

```

**Run**: `python3 main.py` from this example directory.

**Key takeaway**: Keep install clean venv explicit and observable at the Linux application boundary.

---

### Example 72: Test Signal Handling

_ex-72 · `test-signal-handling` · exercises co-30, co-16_

**`learning/code/ex-72-test-signal-handling/main.py`**

```python
"""Test SIGTERM handling in a real child process."""
import os
import signal
import subprocess
import sys


def test_sigterm_stops_cleanly():
    child = subprocess.Popen(
        [sys.executable, "-c", "import signal,time; signal.signal(signal.SIGTERM, lambda *_: exit(0)); time.sleep(5)"]
    )
    os.kill(child.pid, signal.SIGTERM)
    assert child.wait(timeout=2) == 0

```

**Run**: `python3 main.py` from this example directory.

**Key takeaway**: Keep test signal handling explicit and observable at the Linux application boundary.

---

### Example 73: Test Daemon Lifecycle

_ex-73 · `test-daemon-lifecycle` · exercises co-30, co-18_

**`learning/code/ex-73-test-daemon-lifecycle/main.py`**

```python
"""Test a daemon's start/stop state transitions."""

class Daemon:
    def __init__(self):
        self.running = False

    def start(self):
        self.running = True

    def stop(self):
        self.running = False


def test_lifecycle():
    daemon = Daemon()
    daemon.start()
    assert daemon.running
    daemon.stop()
    assert not daemon.running

```

**Run**: `python3 main.py` from this example directory.

**Key takeaway**: Keep test daemon lifecycle explicit and observable at the Linux application boundary.

---

### Example 74: Test Subprocess Error

_ex-74 · `test-subprocess-error` · exercises co-29, co-14_

**`learning/code/ex-74-test-subprocess-error/main.py`**

```python
"""Test an error return from a failing child process."""
import subprocess


def test_child_failure_has_stderr():
    result = subprocess.run(
        ["sh", "-c", "printf broken >&2; exit 7"], capture_output=True, text=True
    )
    assert result.returncode == 7
    assert result.stderr == "broken"

```

**Run**: `pytest main.py` from this example directory.

**Key takeaway**: Keep test subprocess error explicit and observable at the Linux application boundary.

---

### Example 75: Structured Logging

_ex-75 · `structured-logging` · exercises co-08_

**`learning/code/ex-75-structured-logging/main.py`**

```python
"""Emit a structured JSON lifecycle log record."""
import json
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
logging.info(json.dumps({"event": "status_request", "socket": "notes.sock", "result": "ok"}))

```

**Run**: `python3 main.py` from this example directory.

**Key takeaway**: Keep structured logging explicit and observable at the Linux application boundary.

---

### Example 76: Cli Daemon Shared Core

_ex-76 · `cli-daemon-shared-core` · exercises co-18, co-03_

**`learning/code/ex-76-cli-daemon-shared-core/main.py`**

```python
"""Keep the CLI and daemon on one protocol core."""

def status_reply(command: bytes) -> bytes:
    return b"OK notes-daemon" if command == b"STATUS" else b"ERROR unknown command"


print(status_reply(b"STATUS").decode())

```

**Run**: `python3 main.py` from this example directory.

**Key takeaway**: Keep cli daemon shared core explicit and observable at the Linux application boundary.

---

### Example 77: Integration Ipc Slice

_ex-77 · `integration-ipc-slice` · exercises co-25, co-18, co-15_

**`learning/code/ex-77-integration-ipc-slice/main.py`**

```python
"""Exercise one end-to-end Unix-socket request/reply slice."""
import socket
import tempfile
import threading
from pathlib import Path


def reply(server):
    connection, _ = server.accept()
    with connection:
        connection.sendall(b"OK notes-daemon" if connection.recv(32) == b"STATUS" else b"ERROR")


with tempfile.TemporaryDirectory() as directory:
    path = Path(directory) / "ipc.sock"
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as server:
        server.bind(str(path))
        server.listen(1)
        worker = threading.Thread(target=reply, args=(server,))
        worker.start()
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
            client.connect(str(path))
            client.sendall(b"STATUS")
            assert client.recv(32) == b"OK notes-daemon"
        worker.join()
print("integration passed")

```

**Run**: `python3 main.py` from this example directory.

**Key takeaway**: Keep integration ipc slice explicit and observable at the Linux application boundary.

---

### Example 78: Capstone Cli And Daemon

_ex-78 · `capstone-cli-and-daemon` · exercises co-03, co-04, co-08, co-13, co-16, co-17, co-19, co-22, co-28_

**`learning/code/ex-78-capstone-cli-and-daemon/main.py`**

```python
"""Run the actual capstone CLI and daemon as separate Linux processes."""
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

CAPSTONE = Path(__file__).parents[3] / "capstone" / "code"
sys.path.insert(0, str(CAPSTONE))

from notes_linux import cli  # noqa: E402


with tempfile.TemporaryDirectory() as directory:
    path = Path(directory) / "n.sock"
    environment = {**os.environ, "PYTHONPATH": str(CAPSTONE)}
    daemon = subprocess.Popen(
        [sys.executable, "-m", "notes_linux.daemon", "--socket", str(path)],
        env=environment,
    )
    try:
        deadline = time.monotonic() + 2
        while not path.exists() and time.monotonic() < deadline:
            time.sleep(0.01)
        assert path.exists()
        assert cli.main(["status", "--socket", str(path)]) == 0
    finally:
        daemon.terminate()
        daemon.wait(timeout=2)
print("notes-linux CLI reached its daemon")
```

**Run**: `python3 main.py` from this example directory.

**Key takeaway**: Keep capstone cli and daemon explicit and observable at the Linux application boundary.
