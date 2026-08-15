# => Keeps this domain step explicit and reviewable.
"""Example 6: entity identity outlives attribute changes."""

# => Keeps the artifact runnable with explicit dependencies.
from dataclasses import dataclass


# => Uses generated value behaviour so policy is not duplicated.
@dataclass
# => Gives domain rules a single, named home.
class Customer:
    id: str  # => identity decides whether this is the same customer
    # => Keeps this domain step explicit and reviewable.
    name: str

    # => Names policy so callers do not recreate the rule.
    def __eq__(self, other: object) -> bool:
        # => Returns the domain result instead of leaking representation.
        return (
            # => Keeps this domain step explicit and reviewable.
            isinstance(other, Customer) and self.id == other.id
        )  # => names do not decide identity


assert Customer("c-1", "Ada") == Customer("c-1", "Ada Lovelace")  # => continuity wins
print("same customer")  # => Output: same customer
