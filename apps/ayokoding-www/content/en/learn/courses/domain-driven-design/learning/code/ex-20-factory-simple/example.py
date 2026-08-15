# => Keeps this domain step explicit and reviewable.
"""Example 20: a factory returns a ready-to-use customer."""

# => Keeps the artifact runnable with explicit dependencies.
from dataclasses import dataclass


# => Uses generated value behaviour so policy is not duplicated.
@dataclass
# => Gives domain rules a single, named home.
class Customer:
    # => Keeps this domain step explicit and reviewable.
    id: str
    # => Keeps this domain step explicit and reviewable.
    email: str

    # => Uses generated value behaviour so policy is not duplicated.
    @classmethod
    # => Names policy so callers do not recreate the rule.
    def register(cls, id: str, email: str) -> "Customer":
        # => Checks policy before a state change is allowed.
        if "@" not in email:
            raise ValueError("invalid email")  # => factory protects creation rules
        return cls(id, email)  # => callers receive a valid entity


# => Proves the stated business rule is observable.
assert Customer.register("c-1", "a@b.test").id == "c-1"
