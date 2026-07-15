"""Example 32: py-spy dump --pid -- the real py-spy command is documented in this example's
write-up (py-spy needs root here, see ex-29). This target instead registers Python's own
faulthandler dump-on-signal hook (stdlib, no root needed) so its real, live stack can still be
inspected from outside the process without stopping it -- the same underlying goal py-spy dump
serves, using a mechanism the process opts into itself."""

from __future__ import annotations

import faulthandler
import signal
import time

faulthandler.register(
    signal.SIGUSR1
)  # co-14/co-03: dumps the live stack to stderr on SIGUSR1


def stuck_in_a_loop() -> None:
    total = 0
    i = 0
    while True:  # deliberately infinite -- this IS the "hung process"
        total += i
        i += 1
        if i % 50_000_000 == 0:
            time.sleep(
                0.001
            )  # yields briefly so the signal can actually be delivered promptly


if __name__ == "__main__":
    stuck_in_a_loop()
