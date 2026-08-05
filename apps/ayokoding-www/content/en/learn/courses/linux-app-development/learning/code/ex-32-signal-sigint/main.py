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
