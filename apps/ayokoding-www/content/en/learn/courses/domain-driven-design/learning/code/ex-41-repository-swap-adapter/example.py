# => Keeps this domain step explicit and reviewable.
"""Example 41: callers depend on the port, not a storage detail."""

# => Keeps the artifact runnable with explicit dependencies.
from typing import Protocol


# => Gives domain rules a single, named home.
class Store(Protocol):
    # => Names policy so callers do not recreate the rule.
    def save(self, value: str) -> None: ...


# => Gives domain rules a single, named home.
class Memory:
    # => Establishes valid state before callers can rely on it.
    def __init__(self) -> None:
        # => Keeps lifecycle state controlled by the domain object.
        self.value = ""

    # => Names policy so callers do not recreate the rule.
    def save(self, value: str) -> None:
        self.value = value  # => fake adapter implements the same port


# => Names policy so callers do not recreate the rule.
def persist(store: Store) -> None:
    store.save("order")  # => domain caller names only the port


# => Keeps scenario data close to the rule it exercises.
memory = Memory()
# => Keeps this domain step explicit and reviewable.
persist(memory)
# => Proves the stated business rule is observable.
assert memory.value == "order"
