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
