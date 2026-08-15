# => Keeps this domain step explicit and reviewable.
"""Example 2: an order owns its own placement rule."""


# => Gives domain rules a single, named home.
class Order:
    # => Establishes valid state before callers can rely on it.
    def __init__(self, total: int) -> None:
        self.total = total  # => this model names a domain value, not a row column

    # => Names policy so callers do not recreate the rule.
    def can_place(self) -> bool:
        return self.total > 0  # => behaviour protects a rule a table cannot express


order = Order(25)  # => a valid candidate has a positive total
assert order.can_place()  # => callers ask the model, not duplicate the predicate
print(order.can_place())  # => Output: True
