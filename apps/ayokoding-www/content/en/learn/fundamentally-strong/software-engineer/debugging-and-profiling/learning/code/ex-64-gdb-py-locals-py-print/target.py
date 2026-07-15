"""Example 64: the target `gdb`'s `py-locals`/`py-print` commands would read
Python locals from, via CPython's bundled python-gdb.py extension -- gated by
the SAME gdb availability/codesigning limitation documented in ex-63. This
target logs the same value gdb would need to read, so the "verify the value
matches logging" check can still run honestly with a real substitute source.
"""

from __future__ import annotations  # => DD-39 hygiene -- unrelated to gdb itself

import logging  # => co-03: the REAL substitute source of truth -- a logged value gdb's py-print would also read

logging.basicConfig(
    level=logging.INFO, format="%(message)s"
)  # => co-03: bare message format -- matches other examples' style
logger = logging.getLogger(
    __name__
)  # => co-03: a per-module logger, same pattern as ex-52's multi-module example


def compute_and_log(
    x: int, y: int
) -> (
    int
):  # => co-22/co-03: the ONE function gdb's `py-locals` would inspect if attached
    result = (
        x * y + 7
    )  # => co-22: the local value py-print would read from process memory, via python-gdb.py
    logger.info(
        "compute_and_log locals: x=%s y=%s result=%s", x, y, result
    )  # => co-03: the REAL, verifiable substitute
    return result  # => co-22: returned but not printed separately -- the log line above IS the evidence


if (
    __name__ == "__main__"
):  # => guards the module-level call so importing this file stays side-effect-free
    compute_and_log(
        6, 9
    )  # => co-22/co-03: fixed inputs -- reproducible, so the logged result is always the same
