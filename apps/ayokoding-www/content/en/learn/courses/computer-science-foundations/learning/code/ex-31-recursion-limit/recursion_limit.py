# learning/code/ex-31-recursion-limit/recursion_limit.py
"""Example 31: Triggering and Catching RecursionError."""  # => co-17: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

import sys  # => co-17: sys.getrecursionlimit() -- the interpreter's own configured call-stack depth guard


def recurse_forever(depth: int = 0) -> int:  # => co-17: no base case -- deliberately unbounded, to HIT the limit
    """Recurse with no base case, deliberately exceeding the interpreter's recursion limit."""  # => co-17: documents recurse_forever's contract -- no runtime output, just sets its __doc__
    return 1 + recurse_forever(depth + 1)  # => co-17: each call pushes ANOTHER frame -- the stack can't grow forever


if __name__ == "__main__":  # => co-17: entry point -- this block runs only when the file executes directly, not on import
    limit = sys.getrecursionlimit()  # => co-17: this interpreter's configured maximum call-stack depth
    print(f"sys.getrecursionlimit() = {limit}")  # => co-17: the ceiling this run is expected to hit
    raised = False  # => co-17: records whether the interpreter's guard actually fired
    try:  # => co-17: without a base case, this call chain WILL exceed the limit -- expected, not a bug
        recurse_forever()  # => co-17: pushes frames until CPython's own guard raises RecursionError
    except RecursionError as exc:  # => co-17: the exact exception type the interpreter raises for stack exhaustion
        raised = True  # => co-17: confirms the guard fired instead of the process crashing silently
        print(f"caught RecursionError near the configured limit of {limit}: {exc}")  # => co-17: fired, not ignored
    assert raised, "RecursionError must have been raised and caught, near sys.getrecursionlimit()"  # => co-17
    print(f"RecursionError raised near sys.getrecursionlimit(): True")  # => co-17: reached only if the assert passed
    # => co-17: this file is self-verifying: if it exits 0, every assert above passed and the demonstrated claim held
