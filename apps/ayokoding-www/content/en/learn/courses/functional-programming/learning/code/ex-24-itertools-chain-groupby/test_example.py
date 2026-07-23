"""Example 24: pytest verification for chain and groupby Over Data."""

from itertools import chain, groupby


def test_chain_then_groupby() -> None:
    morning = ["apple", "apricot", "banana"]
    evening = ["blueberry", "cherry", "avocado"]
    combined = list(chain(morning, evening))
    grouped = {k: list(v) for k, v in groupby(sorted(combined), key=lambda w: w[0])}
    assert grouped["a"] == ["apple", "apricot", "avocado"]
    assert grouped["b"] == ["banana", "blueberry"]


# => Run: pytest -- Output: 1 passed
