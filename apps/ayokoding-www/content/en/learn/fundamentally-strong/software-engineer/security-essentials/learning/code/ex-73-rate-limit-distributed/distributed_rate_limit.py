# learning/code/ex-73-rate-limit-distributed/distributed_rate_limit.py
"""Example 73: a per-worker local limiter DOUBLES the effective limit; a fakeredis-shared limiter holds ONE global limit (co-27)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the limiter logic itself

import fakeredis  # => co-27: fakeredis 2.36.2 pinned -- an in-memory Redis stand-in, keeps this example self-contained


class LocalRateLimiter:  # => co-27: VULNERABLE -- each worker's counter lives ONLY in its own process memory
    def __init__(
        self, limit: int
    ) -> None:  # => co-27: a real, per-instance limiter -- no shared backend at all
        self.limit = limit  # => co-27: the limit THIS worker enforces, in isolation from every other worker
        self.counts: dict[
            str, int
        ] = {}  # => co-27: real, LOCAL state -- invisible to any other worker instance

    def allow(
        self, key: str
    ) -> (
        bool
    ):  # => co-27: returns True if THIS worker's own local count is still under limit
        self.counts[key] = (
            self.counts.get(key, 0) + 1
        )  # => co-27: increments ONLY this worker's own local counter
        return (
            self.counts[key] <= self.limit
        )  # => co-27: compares against THIS worker's own count -- never the global one


class RedisRateLimiter:  # => co-27: FIXED -- every worker increments the SAME real counter in a shared backend
    def __init__(
        self, redis_client: fakeredis.FakeStrictRedis, limit: int, window_seconds: int
    ) -> None:  # => co-27
        self.redis = redis_client  # => co-27: a real Redis client -- fakeredis here, a real redis-py client in production
        self.limit = limit  # => co-27: the SAME real limit every worker sharing this backend enforces together
        self.window_seconds = window_seconds  # => co-27: the real, shared sliding window every worker's INCR respects

    def allow(
        self, key: str
    ) -> (
        bool
    ):  # => co-27: returns True only if the GLOBAL, shared count is still under limit
        count = self.redis.incr(
            key
        )  # => co-27: a REAL, atomic INCR against the SHARED backend -- not a local dict
        if (
            count == 1
        ):  # => co-27: the FIRST increment for this key -- real, this worker just started a new window
            self.redis.expire(
                key, self.window_seconds
            )  # => co-27: real TTL -- the shared window expires for EVERYONE
        return (
            count <= self.limit
        )  # => co-27: compares against the REAL, GLOBAL count -- visible to every worker


def main() -> (
    None
):  # => co-27: splits 10 real requests across 2 workers, twice -- once local, once fakeredis-shared
    print(
        "=== VULNERABLE: 2 workers, each with its OWN local limiter, limit=5 ==="
    )  # => labels section
    worker1_local = LocalRateLimiter(
        limit=5
    )  # => co-27: worker 1's real, independent, in-memory limiter
    worker2_local = LocalRateLimiter(
        limit=5
    )  # => co-27: worker 2's real, SEPARATE, in-memory limiter -- no sharing
    local_allowed = 0  # => co-27: the REAL, running count of requests allowed across BOTH workers combined
    for request_number in range(
        1, 11
    ):  # => co-27: 10 real, simulated requests for the SAME client key
        worker = (
            worker1_local if request_number % 2 == 1 else worker2_local
        )  # => co-27: alternates -- a real load balancer would do this
        if worker.allow(
            "client:1.2.3.4"
        ):  # => co-27: THIS worker's own, isolated local decision
            local_allowed += 1  # => co-27: real running total, across both workers
    print(
        f"total allowed across BOTH local-state workers: {local_allowed} (limit was supposed to be 5)"
    )  # => co-27: real
    assert (
        local_allowed == 10
    )  # => co-27: proves the effective limit DOUBLED -- 5 per worker, unenforced globally

    print(
        "\n=== FIXED: 2 workers, SAME fakeredis backend via a shared FakeServer, limit=5 ==="
    )  # => labels section
    shared_server = (
        fakeredis.FakeServer()
    )  # => co-27: ONE real, shared in-memory Redis stand-in both workers connect to
    worker1_redis = fakeredis.FakeStrictRedis(
        server=shared_server
    )  # => co-27: worker 1's real client, SAME server
    worker2_redis = fakeredis.FakeStrictRedis(
        server=shared_server
    )  # => co-27: worker 2's real client, the SAME server
    limiter1 = RedisRateLimiter(
        worker1_redis, limit=5, window_seconds=60
    )  # => co-27: worker 1's shared-backend limiter
    limiter2 = RedisRateLimiter(
        worker2_redis, limit=5, window_seconds=60
    )  # => co-27: worker 2's shared-backend limiter
    redis_allowed = 0  # => co-27: the REAL, running count of requests allowed across BOTH workers combined
    for request_number in range(
        1, 11
    ):  # => co-27: the SAME 10 simulated requests, SAME alternating pattern
        limiter = (
            limiter1 if request_number % 2 == 1 else limiter2
        )  # => co-27: alternates between the two REAL limiters
        if limiter.allow(
            "client:1.2.3.4"
        ):  # => co-27: a REAL, shared-backend decision -- visible to the OTHER worker too
            redis_allowed += 1  # => co-27: real running total, across both workers
    print(
        f"total allowed across BOTH shared-backend workers: {redis_allowed} (limit was 5)"
    )  # => co-27: real, correct
    assert (
        redis_allowed == 5
    )  # => co-27: proves the GLOBAL limit really held -- exactly 5, no matter which worker served


if (
    __name__ == "__main__"
):  # => co-27: only runs when launched directly, e.g. `python3 distributed_rate_limit.py`
    main()  # => co-27: runs both real scenarios -- a doubled local limit, then a correctly-shared global limit
