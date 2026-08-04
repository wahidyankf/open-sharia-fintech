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
