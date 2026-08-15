# => Keeps this domain step explicit and reviewable.
"""Example 71: writes and reads optimise for different responsibilities."""


# => Gives domain rules a single, named home.
class Order:
    # => Establishes valid state before callers can rely on it.
    def __init__(self) -> None:
        # => Keeps lifecycle state controlled by the domain object.
        self.status = "draft"

    # => Names policy so callers do not recreate the rule.
    def place(self) -> None:
        self.status = "placed"  # => writes protect the aggregate rule


# => Keeps scenario data close to the rule it exercises.
read_model = {
    # => Keeps this domain step explicit and reviewable.
    "o-1": {"status": "placed", "total": 25}
}  # => reads use a query-shaped projection

# => Keeps scenario data close to the rule it exercises.
order = Order()
# => Keeps this domain step explicit and reviewable.
order.place()
# => Proves the stated business rule is observable.
assert read_model["o-1"]["total"] == 25 and order.status == "placed"
