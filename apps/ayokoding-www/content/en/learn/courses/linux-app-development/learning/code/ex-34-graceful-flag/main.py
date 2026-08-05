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
