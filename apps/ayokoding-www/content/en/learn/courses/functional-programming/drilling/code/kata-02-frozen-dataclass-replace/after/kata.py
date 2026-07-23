"""Kata 2 (after): immutability fix -- dataclasses.replace() builds a NEW record, never mutates."""

from dataclasses import dataclass, replace


@dataclass(frozen=True)
class RetryConfig:
    retries: int
    timeout_seconds: float


config = RetryConfig(retries=1, timeout_seconds=5.0)
updated_config = replace(
    config, retries=5
)  # => a NEW RetryConfig, config itself is untouched
print(config)
print(updated_config)
