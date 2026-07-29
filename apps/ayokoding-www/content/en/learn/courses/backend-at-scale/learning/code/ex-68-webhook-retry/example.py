# pyright: strict
"""Example 68: Webhook -- retry a failed delivery with backoff. (co-32, co-38)

A webhook delivery that fails (the receiver returns non-2xx) is retried with
exponential backoff so successive attempts SPACE OUT rather than hammering an
already-struggling receiver. This example prints the deterministic attempt
schedule (no real sleeping). co-38 names the backoff discipline.
"""

from dataclasses import dataclass  # => a small typed record for one attempt


def backoff_delay(attempt: int, base_seconds: int = 2, cap_seconds: int = 3600) -> int:
    # => co-38: exponential backoff, capped: base * 2^(attempt-1), capped at `cap`
    return min(cap_seconds, base_seconds * (2 ** (attempt - 1)))  # => 2, 4, 8, 16, ... capped


@dataclass  # => co-32/co-38: one delivery attempt and the delay before it
class Attempt:
    number: int  # => 1-based attempt number
    status: int  # => the receiver's HTTP status (non-2xx = retry)
    delay_after: int  # => co-38: seconds to wait before the NEXT attempt


def deliver_with_retries(receiver_statuses: list[int]) -> list[Attempt]:  # => simulate N attempts
    attempts: list[Attempt] = []  # => the recorded schedule
    for number, status in enumerate(receiver_statuses, start=1):  # => one status per attempt
        delay = backoff_delay(number) if not (200 <= status < 300) else 0  # => co-38: backoff only on failure
        attempts.append(Attempt(number=number, status=status, delay_after=delay))  # => record it
        if 200 <= status < 300:  # => success -> stop retrying
            break  # => delivered
    return attempts  # => the full schedule


# The receiver fails 3 times (500), then succeeds (200). Delays space out: 2, 4, 8, then 0.
attempts = deliver_with_retries([500, 500, 500, 200])  # => co-38: 4 attempts total
for a in attempts:  # => print the schedule
    print(f"attempt {a.number}: status={a.status}, wait before next={a.delay_after}s")  # => Output: spaced delays

delays = [a.delay_after for a in attempts]  # => co-38: the backoff schedule
print(f"backoff schedule (s): {delays}")  # => Output: [2, 4, 8, 0]

assert delays == [2, 4, 8, 0]  # => co-38: delays double across failed attempts; 0 once it succeeds
assert attempts[-1].status == 200  # => co-32: eventually delivered
