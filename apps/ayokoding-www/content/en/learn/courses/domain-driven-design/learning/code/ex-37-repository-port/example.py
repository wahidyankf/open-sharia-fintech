# => Keeps this domain step explicit and reviewable.
"""Example 37: the domain owns a repository capability."""

# => Keeps the artifact runnable with explicit dependencies.
from typing import Protocol


# => Gives domain rules a single, named home.
class OrderRepository(Protocol):
    # => Names policy so callers do not recreate the rule.
    def add(
        # => Keeps this domain step explicit and reviewable.
        self,
        # => Keeps the root addressable without exposing storage details.
        order_id: str,
    ) -> None: ...  # => port names the required persistence operation
    # => Names policy so callers do not recreate the rule.
    def get(
        # => Keeps this domain step explicit and reviewable.
        self,
        # => Lets callers request the root through its domain identity.
        order_id: str,
    ) -> str: ...  # => implementation remains outside the domain


print(OrderRepository.__name__)  # => Output: OrderRepository
