"""Example 20: a factory returns a ready-to-use customer."""

from dataclasses import dataclass


@dataclass
class Customer:
    id: str
    email: str

    @classmethod
    def register(cls, id: str, email: str) -> "Customer":
        if "@" not in email:
            raise ValueError("invalid email")  # => factory protects creation rules
        return cls(id, email)  # => callers receive a valid entity


assert Customer.register("c-1", "a@b.test").id == "c-1"
