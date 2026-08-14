"""Example 42: an adapter rebuilds a valid root from stored values."""


class Order:
    def __init__(self, id: str, total: int) -> None:
        if total <= 0:
            raise ValueError(
                "positive total"
            )  # => reconstitution keeps constructor rules
        self.id, self.total = id, total


def reconstitute(row: dict[str, object]) -> Order:
    return Order(str(row["id"]), int(row["total"]))  # => adapter maps storage to domain


assert reconstitute({"id": "o-1", "total": 10}).total == 10
