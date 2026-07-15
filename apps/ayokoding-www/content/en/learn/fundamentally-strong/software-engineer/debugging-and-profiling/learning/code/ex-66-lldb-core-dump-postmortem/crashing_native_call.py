"""Example 66: deliberately trigger a real native (SIGSEGV) crash from Python,
via faulthandler's own built-in test hook -- a real, reproducible native fault,
not a simulation. co-04/co-22: this is the target ex-66's post-mortem analyzes.
"""

from __future__ import annotations  # => DD-39 hygiene -- unrelated to the crash itself

import faulthandler  # => co-04/co-22: stdlib module whose _sigsegv() test hook triggers a REAL segfault, on purpose


def crash_here() -> (
    None
):  # => co-04: a named frame -- shows up as `crash_here` in the real crash backtrace below
    faulthandler._sigsegv()  # => co-04/co-22: a REAL segfault, deliberately -- this IS the seeded fault, not a mock


def main() -> (
    None
):  # => co-04: one frame above crash_here() -- also visible in the real backtrace
    crash_here()  # => co-04/co-22: the ONE call whose crash macOS's crash reporter captures as a real .ips report


if (
    __name__ == "__main__"
):  # => guards the module-level call so importing this file stays side-effect-free
    main()  # => co-04/co-22: the ONE call that produces the real, reproducible native crash
