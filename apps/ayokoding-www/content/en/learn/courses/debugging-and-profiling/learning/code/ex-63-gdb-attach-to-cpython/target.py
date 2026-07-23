"""Example 63: the target process gdb WOULD attach to, if gdb were available and
usable on this host. Left runnable and real so the honest limitation write-up
can still show the same target as ex-29's py-spy attempt and ex-32's faulthandler
substitute -- one consistent process shape across every native-tooling example.
"""

from __future__ import annotations  # => DD-39 hygiene -- unrelated to gdb itself

import time  # => co-22: time.sleep() below keeps this process alive long enough to attach to


def busy_loop() -> (
    None
):  # => co-22: the ONE function `gdb -p <pid>` + `py-bt` would show at the top of its stack
    total = 0  # => a running total -- its value is irrelevant, only the LIVE, LONG-RUNNING process matters here
    i = 0  # => co-22: loop counter -- gives gdb's python-gdb.py extension a real Python frame with real locals
    while True:  # => co-22: runs forever -- a reader has time to `ps`, find the pid, and attempt `gdb -p <pid>`
        total += i  # => co-22: trivial work -- keeps the interpreter genuinely executing bytecode between sleeps
        i += 1  # => co-22: advances the counter every iteration, so `i`'s value keeps changing under gdb's eye
        time.sleep(
            0.01
        )  # => co-22: yields between iterations -- low CPU use while still staying attachable


if (
    __name__ == "__main__"
):  # => guards the module-level call so importing this file stays side-effect-free
    busy_loop()  # => co-22: the ONE call a reader launches in the background before attempting `gdb -p <pid>`
