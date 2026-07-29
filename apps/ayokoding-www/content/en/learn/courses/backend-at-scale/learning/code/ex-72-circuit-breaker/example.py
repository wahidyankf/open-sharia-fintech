# pyright: strict
"""Example 72: Circuit breaker -- trip open, then fail fast, then half-open. (co-37)

A circuit breaker wraps a protected call. Once failures reach a threshold,
the breaker TRIPS OPEN and subsequent calls FAIL FAST (no real call is made)
instead of piling onto a failing dependency. After a cooldown, a HALF-OPEN
probe allows one trial; success closes the breaker. Popularized by Nygard's
Release It! (Fowler, CircuitBreaker).
"""

from dataclasses import dataclass  # => a small typed record for the breaker's state


class CallFailed(Exception):  # => stands in for a real dependency error
    pass


@dataclass  # => co-37: the breaker's mutable state
class CircuitBreaker:
    failure_threshold: int  # => consecutive failures that trip the breaker OPEN
    failures: int = 0  # => current consecutive failure count
    state: str = "closed"  # => "closed" | "open" | "half-open"

    def call(self, fn_succeeds: bool) -> str:  # => invoke the protected call (or fail fast)
        if self.state == "open":  # => co-37: OPEN -> fail fast, no real call
            return "fail-fast (open)"  # => the breaker short-circuits
        if self.state == "half-open":  # => co-37: HALF-OPEN -> exactly one probe
            if fn_succeeds:  # => the probe succeeded
                self.state = "closed"  # => close the breaker
                self.failures = 0  # => reset the failure count
                return "recovered (closed)"  # => healthy again
            self.state = "open"  # => the probe failed -> re-open
            return "fail-fast (re-opened)"  # => still broken
        # => state == "closed": make the real call
        if fn_succeeds:  # => success
            self.failures = 0  # => reset
            return "ok (closed)"  # => healthy
        self.failures += 1  # => count the failure
        if self.failures >= self.failure_threshold:  # => co-37: threshold reached -> TRIP OPEN
            self.state = "open"  # => trip
        return f"failed ({self.state})"  # => the call failed

    def cooldown(self) -> None:  # => move an OPEN breaker to HALF-OPEN for a probe
        if self.state == "open":  # => only after a cooldown
            self.state = "half-open"  # => allow one trial


breaker = CircuitBreaker(failure_threshold=3)  # => co-37: trip after 3 consecutive failures

# Three failures trip the breaker OPEN.
print(breaker.call(False))  # => failed (closed) -- failure 1
print(breaker.call(False))  # => failed (closed) -- failure 2
print(breaker.call(False))  # => co-37: failed (open) -- failure 3 trips it
print(breaker.call(True))  # => co-37: fail-fast (open) -- no real call made while open

breaker.cooldown()  # => move to half-open for one probe
print(breaker.call(True))  # => co-37: recovered (closed) -- the probe succeeded, breaker closed

assert breaker.state == "closed"  # => co-37: the breaker recovered via a half-open probe
