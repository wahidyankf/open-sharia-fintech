# => Keeps this domain step explicit and reviewable.
"""Example 19: value types fail close to the input."""

# => Keeps the artifact runnable with explicit dependencies.
from dataclasses import dataclass


# => Uses generated value behaviour so policy is not duplicated.
@dataclass(frozen=True)
# => Gives domain rules a single, named home.
class CustomerEmail:
    # => Keeps this domain step explicit and reviewable.
    value: str

    # => Names policy so callers do not recreate the rule.
    def __post_init__(self) -> None:
        # => Checks policy before a state change is allowed.
        if "@" not in self.value:
            raise ValueError("email required")  # => validation is not deferred


# => Names policy so callers do not recreate the rule.
def contact(email: CustomerEmail) -> str:
    return f"contact {email.value}"  # => intent is in the type


# => Proves the stated business rule is observable.
assert contact(CustomerEmail("a@b.test")) == "contact a@b.test"
