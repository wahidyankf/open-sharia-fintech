"""Example 41: debugpy: --wait-for-client vs. Attach Later -- the target process.

Usage: python3 target.py wait    (blocks for a client before proceeding)
       python3 target.py nowait  (proceeds immediately, whether or not a client ever attaches)
"""

from __future__ import annotations

import sys
import time

import debugpy

wait = sys.argv[1] == "wait"
debugpy.listen(("127.0.0.1", 15680))
print(f"listening, wait_for_client={wait}", flush=True)
if wait:
    debugpy.wait_for_client()  # co-06: BLOCKS here until a DAP client attaches


def early_startup_work() -> int:
    total = 0
    for i in range(3):
        total += i
    return (
        total  # a breakpoint here only matters if it is set BEFORE this line ever runs
    )


result = (
    early_startup_work()
)  # runs almost immediately at startup -- an "import-time"-style bug
print(f"early_startup_work() = {result}", flush=True)
time.sleep(2)
