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
