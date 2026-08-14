"""Example 19: value types fail close to the input."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CustomerEmail:
    value: str

    def __post_init__(self) -> None:
        if "@" not in self.value:
            raise ValueError("email required")  # => validation is not deferred


def contact(email: CustomerEmail) -> str:
    return f"contact {email.value}"  # => intent is in the type


assert contact(CustomerEmail("a@b.test")) == "contact a@b.test"
