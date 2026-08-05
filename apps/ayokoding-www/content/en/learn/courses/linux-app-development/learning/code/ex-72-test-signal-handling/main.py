"""Test SIGTERM handling in a real child process."""

import os
import signal
import subprocess
import sys


def test_sigterm_stops_cleanly():
    child = subprocess.Popen(
        [
            sys.executable,
            "-c",
            "import signal,time; signal.signal(signal.SIGTERM, lambda *_: exit(0)); time.sleep(5)",
        ]
    )
    os.kill(child.pid, signal.SIGTERM)
    assert child.wait(timeout=2) == 0
