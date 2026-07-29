# pyright: strict
"""Example 36: Fixed-window counter -- the boundary-burst flaw. (co-19)

A fixed-window counter resets at each window boundary (e.g. every 60s). The
flaw: a caller can spend the FULL limit at the end of one window AND the full
limit at the start of the next -- 2x the configured limit in a short span
straddling the boundary.
"""

from dataclasses import dataclass  # => a small typed record for the limiter's state


@dataclass  # => co-19: counts calls within the CURRENT fixed window
class FixedWindow:
    limit: int  # => max calls allowed PER window
    window_seconds: int  # => the window length
    count: int  # => calls so far in the current window
    window_start: int  # => the (injected) clock time at which the current window began


def allow(fw: FixedWindow, now: int) -> bool:  # => co-19: count one call, resetting on a window boundary
    if now >= fw.window_start + fw.window_seconds:  # => crossed into a NEW window -> reset the counter
        fw.window_start = now  # => the new window begins now
        fw.count = 0  # => reset
    if fw.count >= fw.limit:  # => this window is exhausted
        return False  # => denied
    fw.count += 1  # => count the call
    return True  # => allowed


fw = FixedWindow(limit=10, window_seconds=60, count=0, window_start=0)  # => co-19: 10 calls per 60s window

# t=58: spend the WHOLE limit at the tail end of window [0,60).
tail = sum(1 for _ in range(10) if allow(fw, now=58))  # => all 10 allowed in window 0
print(f"window 0, 10 calls at t=58: allowed={tail}")  # => Output: 10

eleventh = allow(fw, now=58)  # => window 0 exhausted -> denied
print(f"11th call still in window 0: {eleventh}")  # => Output: False

# t=60: a NEW window begins immediately -> the counter resets -> another 10 allowed.
head = sum(1 for _ in range(10) if allow(fw, now=60))  # => co-19: 10 MORE allowed at the start of window 1
print(f"window 1, 10 calls at t=60: allowed={head}")  # => Output: 10 -- the boundary burst

# In the 2-second span t=[58,60) the caller got 20 calls -- 2x the configured limit. That is the flaw.
boundary_burst = tail + head  # => co-19: 20 calls in ~2 seconds despite limit=10/window
print(f"calls in the 2s boundary span t=[58,60): {boundary_burst} (2x the limit)")  # => Output: 20

assert boundary_burst == 20 and eleventh is False  # => co-19: fixed window suffers 2x at the boundary
