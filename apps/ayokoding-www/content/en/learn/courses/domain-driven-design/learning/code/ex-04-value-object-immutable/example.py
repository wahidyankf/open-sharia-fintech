# => Keeps this domain step explicit and reviewable.
"""Example 4: freezing prevents an invalid in-place edit."""

# => Keeps the artifact runnable with explicit dependencies.
from dataclasses import FrozenInstanceError, dataclass


# => Uses generated value behaviour so policy is not duplicated.
@dataclass(frozen=True)
# => Gives domain rules a single, named home.
class Money:
    amount: int  # => this valid value has no mutable setter


cash = Money(10)  # => construction creates a complete value
# => Separates the expected failure path from valid flow.
try:
    cash.amount = 20  # type: ignore[misc]  # => an in-place rewrite is forbidden
# => Turns the rejected case into an explicit outcome.
except FrozenInstanceError:
    print("immutable")  # => Output: immutable
