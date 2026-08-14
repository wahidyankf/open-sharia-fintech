# => Keeps this domain step explicit and reviewable.
"""Example 56: repositories can accept a domain predicate."""


# => Gives domain rules a single, named home.
class Orders:
    # => Establishes valid state before callers can rely on it.
    def __init__(self, totals: list[int]) -> None:
        # => Keeps lifecycle state controlled by the domain object.
        self.totals = totals

    # => Names policy so callers do not recreate the rule.
    def matching(self, predicate: object) -> list[int]:
        # => Returns the domain result instead of leaking representation.
        return [total for total in self.totals if predicate(total)]  # type: ignore[operator]


# => Keeps scenario data close to the rule it exercises.
orders = Orders([10, 100, 250])
# => Proves the stated business rule is observable.
assert orders.matching(lambda total: total >= 100) == [100, 250]
