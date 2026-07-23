"""Kata 2 (before): immutability violation -- direct attribute assignment on a frozen dataclass."""

from dataclasses import dataclass


@dataclass(frozen=True)
class RetryConfig:
    retries: int
    timeout_seconds: float


config = RetryConfig(retries=1, timeout_seconds=5.0)
config.retries = 5  # type: ignore[misc]  # BUG: frozen dataclasses reject assignment -- raises at runtime
print(config)
