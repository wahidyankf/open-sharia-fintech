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
