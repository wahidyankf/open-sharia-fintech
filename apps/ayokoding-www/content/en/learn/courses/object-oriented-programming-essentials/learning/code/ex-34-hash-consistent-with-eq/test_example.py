"""Example 34: pytest verification for A Consistent __hash__ Alongside __eq__."""

from example import Money


def test_equal_money_objects_deduplicate_in_a_set() -> None:
    wallet: set[Money] = {Money(500, "USD"), Money(500, "USD"), Money(100, "USD")}
    assert len(wallet) == 2  # => the duplicate Money(500, "USD") collapses to one entry


def test_equal_objects_share_a_hash() -> None:
    assert hash(Money(500, "USD")) == hash(
        Money(500, "USD")
    )  # => required by the eq/hash contract


# => Run: pytest -- Output: 2 passed
