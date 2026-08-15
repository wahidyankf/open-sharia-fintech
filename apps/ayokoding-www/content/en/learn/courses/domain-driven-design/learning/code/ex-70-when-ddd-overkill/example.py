# => Keeps this domain step explicit and reviewable.
"""Example 70: a simple address book needs no aggregate ceremony."""

# => Keeps the artifact runnable with explicit dependencies.
from dataclasses import dataclass


# => Uses generated value behaviour so policy is not duplicated.
@dataclass
# => Gives domain rules a single, named home.
class Contact:
    # => Keeps this domain step explicit and reviewable.
    name: str
    phone: str  # => plain data is sufficient when there are no complex invariants


# => Proves the stated business rule is observable.
assert Contact("Ada", "123").name == "Ada"
