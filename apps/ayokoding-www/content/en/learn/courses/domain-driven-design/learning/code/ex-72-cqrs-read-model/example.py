# => Keeps this domain step explicit and reviewable.
"""Example 72: a projection answers a query without loading an aggregate."""

# => Keeps scenario data close to the rule it exercises.
summaries = [
    # => Keeps this domain step explicit and reviewable.
    {"order_id": "o-1", "total": 25, "status": "placed"}
]  # => denormalised query representation


# => Names policy so callers do not recreate the rule.
def find_summary(order_id: str) -> dict[str, object]:
    # => Returns the domain result instead of leaking representation.
    return next(row for row in summaries if row["order_id"] == order_id)


# => Proves the stated business rule is observable.
assert find_summary("o-1")["status"] == "placed"
