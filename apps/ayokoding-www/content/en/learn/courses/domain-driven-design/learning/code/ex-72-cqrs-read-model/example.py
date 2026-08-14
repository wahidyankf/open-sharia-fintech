"""Example 72: a projection answers a query without loading an aggregate."""

summaries = [
    {"order_id": "o-1", "total": 25, "status": "placed"}
]  # => denormalised query representation


def find_summary(order_id: str) -> dict[str, object]:
    return next(row for row in summaries if row["order_id"] == order_id)


assert find_summary("o-1")["status"] == "placed"
