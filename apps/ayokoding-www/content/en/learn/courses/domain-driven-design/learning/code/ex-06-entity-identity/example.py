"""Example 6: entity identity outlives attribute changes."""

from dataclasses import dataclass


@dataclass
class Customer:
    id: str  # => identity decides whether this is the same customer
    name: str

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Customer) and self.id == other.id
        )  # => names do not decide identity


assert Customer("c-1", "Ada") == Customer("c-1", "Ada Lovelace")  # => continuity wins
print("same customer")  # => Output: same customer
