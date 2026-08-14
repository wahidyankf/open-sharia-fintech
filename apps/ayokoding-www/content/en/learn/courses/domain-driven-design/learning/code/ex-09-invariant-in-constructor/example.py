"""Example 9: construction rejects an impossible currency."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
    amount: int
    currency: str

    def __post_init__(self) -> None:
        if self.currency not in {"USD", "IDR"}:  # => valid currencies are an invariant
            raise ValueError(
                "unknown currency"
            )  # => invalid values never escape construction


try:
    Money(10, "NOPE")
except ValueError as error:
    print(str(error))  # => Output: unknown currency
