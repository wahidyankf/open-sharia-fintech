# => Keeps this domain step explicit and reviewable.
"""Example 12: email validation belongs in the value object."""

# => Keeps the artifact runnable with explicit dependencies.
from dataclasses import dataclass


# => Uses generated value behaviour so policy is not duplicated.
@dataclass(frozen=True)
# => Gives domain rules a single, named home.
class Email:
    # => Keeps this domain step explicit and reviewable.
    value: str

    # => Names policy so callers do not recreate the rule.
    def __post_init__(self) -> None:
        # => Checks policy before a state change is allowed.
        if "@" not in self.value:
            raise ValueError("invalid email")  # => malformed input cannot travel


# => Proves the stated business rule is observable.
assert Email("ada@example.test").value.endswith(
    # => Keeps this domain step explicit and reviewable.
    ".test"
)  # => accepted data is usable immediately
# => Separates the expected failure path from valid flow.
try:
    # => Keeps this domain step explicit and reviewable.
    Email("not-an-email")
# => Turns the rejected case into an explicit outcome.
except ValueError:
    print("invalid email")  # => Output: invalid email
