# pyright: strict
"""Example 35: Leaky-bucket rate limiter. (co-19)

A leaky bucket holds requests in a queue that DRAINS at a constant rate,
smoothing bursts into a steady output stream. A burst arrives all at once
but is spaced out to the drain rate. The clock is INJECTED for determinism.
"""

from dataclasses import dataclass  # => a small typed record for the limiter's state


@dataclass  # => co-19: the bucket's mutable state
class LeakyBucket:
    drain_rate: float  # => requests drained (processed) per second -- the smoothed output rate
    queue: list[float]  # => arrival timestamps of queued requests
    capacity: int  # => max queued requests before new arrivals are rejected
    last_drain: float  # => the (injected) clock time of the last drain computation


def drain(bucket: LeakyBucket, now: float) -> None:  # => co-19: remove requests that have "drained out" by now
    elapsed = now - bucket.last_drain  # => seconds passed since the last drain
    processed = int(elapsed * bucket.drain_rate)  # => how many requests drained in that window
    bucket.queue = bucket.queue[processed:]  # => drop the drained requests from the front
    bucket.last_drain = now  # => advance the drain timestamp


def admit(bucket: LeakyBucket, now: float) -> bool:  # => co-19: enqueue a request if room remains
    drain(bucket, now)  # => first drain whatever elapsed
    if len(bucket.queue) >= bucket.capacity:  # => queue full -> reject (backpressure)
        return False  # => denied
    bucket.queue.append(now)  # => enqueue this request's arrival
    return True  # => admitted (will be smoothed out at drain_rate)


bucket = LeakyBucket(drain_rate=2.0, queue=[], capacity=3, last_drain=0.0)  # => co-19: drains 2/sec, holds 3

# t=0: a burst of 5 arrives; only 3 fit the capacity, 2 are rejected.
results = [admit(bucket, now=0.0) for _ in range(5)]  # => 3 admitted, 2 rejected
print(f"burst of 5 at t=0: admitted={sum(results)}, rejected={5 - sum(results)}")  # => Output: 3, 2

# t=1: 1 second elapsed -> 2 requests drained out, making room for ~2 new.
after_drain = admit(bucket, now=1.0)  # => co-19: room freed by the constant drain -> admitted
print(f"call at t=1 (after drain): {after_drain}")  # => Output: True -- smoothed output makes room

assert sum(results) == 3 and after_drain is True  # => co-19: bursts smoothed to the drain rate over time
