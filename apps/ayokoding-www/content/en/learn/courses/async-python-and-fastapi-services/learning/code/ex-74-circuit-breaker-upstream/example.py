"""Example 74: A Circuit Breaker Around an Upstream.

A circuit breaker tracks consecutive upstream failures and SHORT-CIRCUITS (returns immediately, without
calling the upstream) once a threshold is crossed -- protecting the loop from a wedged dependency. Run:
python3 example.py. (co-17, co-06)
"""

import asyncio  # => asyncio.sleep simulates upstream latency (co-02)


class CircuitOpenError(Exception):  # => raised when the circuit is open (co-17)
    pass


class CircuitBreaker:  # => a small state machine: CLOSED -> OPEN -> (half-open retry) (co-06)
    def __init__(self, threshold: int = 3) -> None:  # => threshold consecutive failures open the circuit
        self.threshold = threshold  # => the failure count that trips the breaker
        self.failures = 0  # => consecutive failure counter
        self.open = False  # => start CLOSED (calling the upstream)

    async def call(self, upstream) -> object:  # => call the upstream THROUGH the breaker
        if self.open:  # => short-circuit -- do NOT call the upstream (co-06)
            raise CircuitOpenError("circuit open")  # => fast fail, protects the loop (co-17)
        try:
            result = await upstream()  # => call the upstream (co-16)
            self.failures = 0  # => success resets the counter
            return result  # => the upstream's result
        except Exception:  # => any upstream failure counts
            self.failures += 1  # => one more consecutive failure
            if self.failures >= self.threshold:  # => crossed the threshold
                self.open = True  # => OPEN the circuit -- subsequent calls short-circuit (co-06)
            raise  # => re-raise the original failure (co-17)


async def flaky_upstream() -> str:  # => an upstream that always fails for this demo
    await asyncio.sleep(0.01)  # => simulate latency (co-02)
    raise RuntimeError("upstream down")  # => always fails -> trips the breaker after `threshold` calls


async def main() -> None:  # => demonstrates CLOSED -> OPEN, then short-circuit
    breaker = CircuitBreaker(threshold=3)  # => open after 3 failures
    failures = 0  # => count calls that raised the upstream error
    opens = 0  # => count calls that short-circuited (CircuitOpenError)
    for _ in range(5):  # => 5 calls total
        try:
            await breaker.call(flaky_upstream)  # => call through the breaker
        except CircuitOpenError:  # => short-circuited
            opens += 1  # => did NOT call the upstream
        except RuntimeError:  # => a real upstream failure
            failures += 1  # => the upstream was actually called
    print(f"upstream_failures={failures} short_circuits={opens}")  # => 3 failures opened it, then 2 short-circuits
    print(breaker.open)  # => Output: True -- the circuit is now open


if __name__ == "__main__":  # => run directly
    asyncio.run(main())
