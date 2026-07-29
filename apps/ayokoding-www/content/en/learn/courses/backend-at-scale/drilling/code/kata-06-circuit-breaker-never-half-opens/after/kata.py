# pyright: strict
"""Kata 6 (after): circuit breaker closes on a successful half-open probe."""

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
            # THE FIX: a half-open probe CLOSES on success and re-OPENS on failure.
            if fn_succeeds:
                self.state = "closed"
                self.failures = 0
                return "recovered (closed)"
            self.state = "open"
            return "fail-fast (re-opened)"
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
print(b.call(True))  # recovered (closed) -- the probe closed the breaker
assert b.state == "closed"
