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
