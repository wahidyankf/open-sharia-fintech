# => Keeps this domain step explicit and reviewable.
"""Example 42: an adapter rebuilds a valid root from stored values."""


# => Gives domain rules a single, named home.
class Order:
    # => Establishes valid state before callers can rely on it.
    def __init__(self, id: str, total: int) -> None:
        # => Checks policy before a state change is allowed.
        if total <= 0:
            # => Stops invalid business state at the boundary.
            raise ValueError(
                # => Keeps this domain step explicit and reviewable.
                "positive total"
            )  # => reconstitution keeps constructor rules
        # => Keeps lifecycle state controlled by the domain object.
        self.id, self.total = id, total


# => Names policy so callers do not recreate the rule.
def reconstitute(row: dict[str, object]) -> Order:
    return Order(str(row["id"]), int(row["total"]))  # => adapter maps storage to domain


# => Proves the stated business rule is observable.
assert reconstitute({"id": "o-1", "total": 10}).total == 10
