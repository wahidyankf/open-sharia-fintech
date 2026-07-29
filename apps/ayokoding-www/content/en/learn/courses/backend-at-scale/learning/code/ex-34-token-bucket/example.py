# pyright: strict
"""Example 34: Token-bucket rate limiter. (co-19)

A token bucket holds up to `capacity` tokens and refills at `rate` per
second; each call consumes one token. It ALLOWS BURSTS up to capacity (a
client may spend a full bucket at once), then throttles to the refill rate.
AWS API Gateway uses this algorithm. The clock is INJECTED so output is
deterministic.
"""

from dataclasses import dataclass  # => a small typed record for the limiter's state


@dataclass  # => co-19: the bucket's mutable state
class TokenBucket:
    capacity: int  # => the max tokens the bucket can hold (burst size)
    rate: float  # => tokens added per second (steady-state throughput)
    tokens: float  # => current token count
    last_refill: float  # => the (injected) clock time of the last refill computation


def refill(bucket: TokenBucket, now: float) -> None:  # => co-19: add tokens elapsed since the last refill
    elapsed = now - bucket.last_refill  # => seconds passed since the last refill
    bucket.tokens = min(bucket.capacity, bucket.tokens + elapsed * bucket.rate)  # => refill, capped at capacity
    bucket.last_refill = now  # => advance the refill timestamp


def allow(bucket: TokenBucket, now: float) -> bool:  # => co-19: consume one token if available
    refill(bucket, now)  # => top up the bucket for elapsed time first
    if bucket.tokens >= 1.0:  # => enough tokens -> consume one
        bucket.tokens -= 1.0  # => consume
        return True  # => allowed
    return False  # => empty bucket -> denied (throttled)


bucket = TokenBucket(capacity=5, rate=1.0, tokens=5.0, last_refill=0.0)  # => co-19: 5-token burst, refills 1/sec

# t=0: a burst of 5 calls empties the bucket.
burst = [allow(bucket, now=0.0) for _ in range(5)]  # => all 5 succeed (capacity allows the burst)
print(f"burst of 5 at t=0: allowed={sum(burst)}")  # => Output: 5

denied = allow(bucket, now=0.0)  # => bucket empty at t=0 -> denied
print(f"6th call at t=0: {denied}")  # => Output: False -- throttled

# t=3: 3 seconds elapsed -> ~3 tokens refilled.
refilled = allow(bucket, now=3.0)  # => ~3 tokens available after refill -> allowed
print(f"call at t=3 (after refill): {refilled}")  # => Output: True -- tokens refilled over time

assert sum(burst) == 5 and denied is False and refilled is True  # => co-19: bursts allowed, then refill over time
