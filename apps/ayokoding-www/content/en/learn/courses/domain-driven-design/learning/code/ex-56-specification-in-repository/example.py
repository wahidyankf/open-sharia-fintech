"""Example 56: repositories can accept a domain predicate."""


class Orders:
    def __init__(self, totals: list[int]) -> None:
        self.totals = totals

    def matching(self, predicate: object) -> list[int]:
        return [total for total in self.totals if predicate(total)]  # type: ignore[operator]


orders = Orders([10, 100, 250])
assert orders.matching(lambda total: total >= 100) == [100, 250]
