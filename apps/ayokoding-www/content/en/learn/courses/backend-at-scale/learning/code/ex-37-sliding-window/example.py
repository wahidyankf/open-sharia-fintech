# pyright: strict
"""Example 37: Sliding-window rate limiter -- no boundary burst. (co-19)

A sliding window counts requests in a TRAILING window ending at NOW, so a
burst straddling a former boundary is still bounded by the limit (no 2x
flaw). This is the algorithm Cloudflare uses in production.
"""

from collections import deque  # => deque: efficient popleft of aged-out timestamps
from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => co-19: keeps the timestamp of every call within the trailing window
class SlidingWindow:
    limit: int  # => max calls in ANY trailing window of `window_seconds`
    window_seconds: int  # => the trailing window length
    events: deque[int] = field(default_factory=deque[int])  # => call timestamps, oldest first


def allow(sw: SlidingWindow, now: int) -> bool:  # => co-19: count calls in [now-window, now]
    cutoff = now - sw.window_seconds  # => the oldest timestamp still inside the trailing window
    while sw.events and sw.events[0] <= cutoff:  # => drop timestamps that have aged out of the window
        sw.events.popleft()  # => remove the aged event
    if len(sw.events) >= sw.limit:  # => the trailing window is already full
        return False  # => denied
    sw.events.append(now)  # => record this call's timestamp
    return True  # => allowed


sw = SlidingWindow(limit=10, window_seconds=60)  # => co-19: 10 calls in any trailing 60s

# t=58: spend the whole limit at the tail of a span.
tail = sum(1 for _ in range(10) if allow(sw, now=58))  # => all 10 allowed
print(f"10 calls at t=58: allowed={tail}")  # => Output: 10

# t=60: only 2 seconds later, the trailing 60s window [0,60) STILL contains all 10 from t=58.
after = allow(sw, now=60)  # => co-19: the window is still full -> denied (no reset, no 2x burst)
print(f"call at t=60 (2s later): {after}")  # => Output: False -- the sliding window did NOT reset

# t=119: 61s after the t=58 burst, those calls have aged out -> room again.
freed = allow(sw, now=119)  # => co-19: the trailing window no longer holds the t=58 calls -> allowed
print(f"call at t=119 (61s after the burst): {freed}")  # => Output: True

assert tail == 10 and after is False and freed is True  # => co-19: avoids the fixed-window boundary burst
