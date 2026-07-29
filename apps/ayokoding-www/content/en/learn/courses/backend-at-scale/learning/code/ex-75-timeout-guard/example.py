# pyright: strict
"""Example 75: Timeout guard -- abort a slow call at a deadline. (co-39)

A timeout caps how long a call may wait. If the operation does not finish by
the deadline, it ABORTS with a timeout error rather than hanging indefinitely
and tying up a request thread. The "clock" is the operation's reported
duration, so the abort is deterministic.
"""

from dataclasses import dataclass  # => a small typed record for the result


class TimeoutError(Exception):  # => stands in for a deadline-exceeded error
    pass


@dataclass  # => co-39: the outcome -- either a value or a timeout
class Result:
    status: str  # => "ok" or "timeout"
    value: str = ""  # => the value on success (empty on timeout)


def call_with_timeout(op_duration: float, deadline: float) -> Result:  # => co-39: abort if op_duration exceeds deadline
    if op_duration > deadline:  # => co-39: the operation outlasted the deadline -> abort
        return Result(status="timeout")  # => aborted at the deadline (no full wait)
    return Result(status="ok", value=f"completed in {op_duration}")  # => finished within the deadline


fast = call_with_timeout(op_duration=0.2, deadline=1.0)  # => finishes well within the deadline
print(f"fast call (0.2s, deadline 1.0s): {fast.status}, {fast.value!r}")  # => Output: ok

slow = call_with_timeout(op_duration=5.0, deadline=1.0)  # => co-39: would take 5s -> aborted at the 1s deadline
print(f"slow call (5.0s, deadline 1.0s): {slow.status}")  # => Output: timeout -- aborted, did NOT wait 5s

assert fast.status == "ok" and slow.status == "timeout"  # => co-39: the deadline aborted the slow call
