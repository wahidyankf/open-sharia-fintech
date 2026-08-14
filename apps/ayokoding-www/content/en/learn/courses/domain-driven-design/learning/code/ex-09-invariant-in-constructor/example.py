# => Keeps this domain step explicit and reviewable.
"""Example 9: construction rejects an impossible currency."""

# => Keeps the artifact runnable with explicit dependencies.
from dataclasses import dataclass


# => Uses generated value behaviour so policy is not duplicated.
@dataclass(frozen=True)
# => Gives domain rules a single, named home.
class Money:
    # => Keeps this domain step explicit and reviewable.
    amount: int
    # => Keeps this domain step explicit and reviewable.
    currency: str

    # => Names policy so callers do not recreate the rule.
    def __post_init__(self) -> None:
        if self.currency not in {"USD", "IDR"}:  # => valid currencies are an invariant
            # => Stops invalid business state at the boundary.
            raise ValueError(
                # => Keeps this domain step explicit and reviewable.
                "unknown currency"
            )  # => invalid values never escape construction


# => Separates the expected failure path from valid flow.
try:
    # => Keeps this domain step explicit and reviewable.
    Money(10, "NOPE")
# => Turns the rejected case into an explicit outcome.
except ValueError as error:
    print(str(error))  # => Output: unknown currency
