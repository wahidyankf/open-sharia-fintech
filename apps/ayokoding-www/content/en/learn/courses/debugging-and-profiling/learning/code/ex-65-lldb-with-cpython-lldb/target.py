"""Example 65: the target lldb + cpython_lldb's `py-bt` would inspect, if a live
`lldb -p <pid>` attach were usable on this host (see the real, captured
limitation evidence in this example's write-up -- macOS Developer Mode is
disabled, and lldb attach hangs waiting on an authorization step this headless
sandbox cannot satisfy).
"""

from __future__ import annotations  # => DD-39 hygiene -- unrelated to lldb itself

import time  # => co-22: time.sleep() below keeps this process alive long enough to ATTEMPT an attach


def busy_loop() -> (
    None
):  # => co-22: the SAME shape as ex-63's target -- a real, long-running Python frame
    total = 0  # => a running total -- its value is irrelevant, only the LIVE process matters here
    i = 0  # => co-22: loop counter -- gives cpython_lldb's `py-bt` a real Python frame to walk, if attach succeeded
    while True:  # => co-22: runs forever -- a reader has time to `ps`, find the pid, and attempt `lldb -p <pid>`
        total += i  # => co-22: trivial work -- keeps the interpreter genuinely executing bytecode between sleeps
        i += 1  # => co-22: advances the counter every iteration
        time.sleep(
            0.01
        )  # => co-22: yields between iterations -- low CPU use while still staying attachable


if (
    __name__ == "__main__"
):  # => guards the module-level call so importing this file stays side-effect-free
    busy_loop()  # => co-22: the ONE call a reader launches in the background before attempting `lldb -p <pid>`
