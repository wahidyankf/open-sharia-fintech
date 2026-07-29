# pyright: strict
"""Kata 6 (before): circuit breaker never leaves the HALF-OPEN state."""

from dataclasses import dataclass


@dataclass
class CircuitBreaker:
    failure_threshold: int
    failures: int = 0
    state: str = "closed"

    def call(self, fn_succeeds: bool) -> str:
        if self.state == "open":
            return "fail-fast (open)"
        if self.state == "half-open":
            # THE BUG: a half-open probe NEVER closes on success and NEVER re-opens on
            # failure -- the breaker is stuck half-open forever, so recovery never completes.
            return "stuck (half-open)"  # BUG: no transition out of half-open
        if fn_succeeds:
            self.failures = 0
            return "ok (closed)"
        self.failures += 1
        if self.failures >= self.failure_threshold:
            self.state = "open"
        return f"failed ({self.state})"

    def cooldown(self) -> None:
        if self.state == "open":
            self.state = "half-open"


b = CircuitBreaker(failure_threshold=2)
print(b.call(False))  # failed (closed)
print(b.call(False))  # failed (open) -- trips
b.cooldown()  # -> half-open
print(b.call(True))  # BUG: stuck (half-open) -- a success should CLOSE the breaker
