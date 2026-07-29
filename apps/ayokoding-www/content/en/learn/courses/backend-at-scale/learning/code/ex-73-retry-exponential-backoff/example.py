# pyright: strict
"""Example 73: Retry with exponential backoff. (co-38)

Retrying a transient failure with exponential backoff DOUBLES the wait
between attempts (base * 2^attempt). The delays space out -- but plain
backoff CLUSTERS retries when many clients fail at once (the flaw Example 74
fixes with jitter). Delays are computed, not slept, so output is deterministic.
"""

from dataclasses import dataclass  # => a small typed record for the schedule


def backoff_delay(attempt: int, base_seconds: float = 1.0, cap_seconds: float = 32.0) -> float:
    # => co-38: exponential backoff: base * 2^(attempt-1), capped at `cap`
    return min(cap_seconds, base_seconds * (2 ** (attempt - 1)))  # => 1, 2, 4, 8, 16, 32, 32, ...


@dataclass  # => co-38: one attempt's wait before the next retry
class ScheduledWait:
    attempt: int  # => 1-based attempt number
    wait_before_next: float  # => seconds waited BEFORE the next attempt


def schedule(max_attempts: int) -> list[ScheduledWait]:  # => compute the full backoff schedule
    return [ScheduledWait(attempt=n, wait_before_next=backoff_delay(n)) for n in range(1, max_attempts + 1)]  # => co-38


plan = schedule(max_attempts=6)  # => co-38: a 6-attempt schedule
for step in plan:  # => print each step
    print(f"attempt {step.attempt}: wait before next = {step.wait_before_next}s")  # => Output: doubling waits

waits = [step.wait_before_next for step in plan]  # => co-38: the delay sequence
print(f"delays: {waits}")  # => Output: [1, 2, 4, 8, 16, 32]

assert waits == [1, 2, 4, 8, 16, 32]  # => co-38: each delay doubles, capped at 32
