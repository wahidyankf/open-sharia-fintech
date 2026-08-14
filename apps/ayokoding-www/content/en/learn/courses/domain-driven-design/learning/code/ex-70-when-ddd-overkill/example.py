"""Example 70: a simple address book needs no aggregate ceremony."""

from dataclasses import dataclass


@dataclass
class Contact:
    name: str
    phone: str  # => plain data is sufficient when there are no complex invariants


assert Contact("Ada", "123").name == "Ada"
