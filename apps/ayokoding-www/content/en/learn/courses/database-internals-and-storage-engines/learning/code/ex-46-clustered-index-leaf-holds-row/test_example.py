"""Example 46: pytest verification for Clustered Index Leaves Holding the Full Row."""

from example import Row, clustered_lookup


def test_pk_lookup_returns_the_full_row() -> None:
    index = {5: Row(id=5, name="Carol", email="carol@example.com")}
    row = clustered_lookup(index, pk=5)
    assert row is not None
    assert row.email == "carol@example.com"


def test_pk_lookup_needs_exactly_one_fetch() -> None:
    import example

    example.fetch_count = 0
    index = {1: Row(id=1, name="A", email="a@example.com")}
    clustered_lookup(index, pk=1)
    assert example.fetch_count == 1


# => Run: pytest -- Output: 2 passed
