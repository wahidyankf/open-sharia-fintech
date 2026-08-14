"""Example 33: orders stay separate from customer identity."""


class Customer:
    def __init__(self, id: str) -> None:
        self.id = id  # => customer protects its own profile facts


class Order:
    def __init__(self, customer_id: str) -> None:
        self.customer_id = customer_id  # => order does not load history


assert (
    Order(Customer("c-1").id).customer_id == "c-1"
)  # => small roots reduce contention
