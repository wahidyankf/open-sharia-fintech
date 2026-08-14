"""Example 4: freezing prevents an invalid in-place edit."""

from dataclasses import FrozenInstanceError, dataclass


@dataclass(frozen=True)
class Money:
    amount: int  # => this valid value has no mutable setter


cash = Money(10)  # => construction creates a complete value
try:
    cash.amount = 20  # type: ignore[misc]  # => an in-place rewrite is forbidden
except FrozenInstanceError:
    print("immutable")  # => Output: immutable
