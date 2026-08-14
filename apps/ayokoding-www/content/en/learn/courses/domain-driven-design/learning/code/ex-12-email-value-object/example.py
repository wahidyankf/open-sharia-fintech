"""Example 12: email validation belongs in the value object."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self) -> None:
        if "@" not in self.value:
            raise ValueError("invalid email")  # => malformed input cannot travel


assert Email("ada@example.test").value.endswith(
    ".test"
)  # => accepted data is usable immediately
try:
    Email("not-an-email")
except ValueError:
    print("invalid email")  # => Output: invalid email
