# => Keeps this domain step explicit and reviewable.
"""Example 33: orders stay separate from customer identity."""


# => Gives domain rules a single, named home.
class Customer:
    # => Establishes valid state before callers can rely on it.
    def __init__(self, id: str) -> None:
        self.id = id  # => customer protects its own profile facts


# => Gives domain rules a single, named home.
class Order:
    # => Establishes valid state before callers can rely on it.
    def __init__(self, customer_id: str) -> None:
        self.customer_id = customer_id  # => order does not load history


# => Proves the stated business rule is observable.
assert (
    # => Keeps this domain step explicit and reviewable.
    Order(Customer("c-1").id).customer_id == "c-1"
)  # => small roots reduce contention
