"""Example 71: the target `py-spy record --native` would sample -- a workload
that calls into a real C extension (hashlib), so a native-aware profiler would
show mixed Python+native frames if it could attach on this host.
"""

from __future__ import annotations  # => DD-39 hygiene -- unrelated to py-spy itself

import hashlib  # => co-14/co-19/co-22: a REAL C extension -- the native frame `--native` would try to surface
import time  # => co-14: time.sleep() below keeps this process alive long enough to attach to


def hash_loop() -> (
    None
):  # => co-14/co-19: the ONE function `py-spy record --native` would sample, if it could attach
    data = (
        b"x" * 4096
    )  # => co-14: a fixed-size payload -- keeps each sha256 call's cost consistent across iterations
    while True:  # => co-14: runs forever -- a reader has time to `ps`, find the pid, and attempt `py-spy record`
        hashlib.sha256(
            data
        ).digest()  # => co-14/co-19/co-22: the C-extension call -- would show as a NATIVE frame under Python
        time.sleep(
            0.001
        )  # => co-14: small yield between iterations -- keeps this a real, sustained, attachable workload


if (
    __name__ == "__main__"
):  # => guards the module-level call so importing this file stays side-effect-free
    hash_loop()  # => co-14/co-19: the ONE call a reader launches in the background before attempting `py-spy record --native`
