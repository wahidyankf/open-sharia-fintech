"""Example 73: pytest verification for Value Objects Deduplicate Inside a Set."""

from example import Money


def test_duplicate_value_objects_collapse_in_a_set() -> None:
    payments: list[Money] = [
        Money(500, "USD"),
        Money(500, "USD"),
        Money(100, "USD"),
        Money(500, "EUR"),
    ]
    unique: set[Money] = set(payments)
    assert len(unique) == 3  # => only the exact duplicate collapsed


# => Run: pytest -- Output: 1 passed
