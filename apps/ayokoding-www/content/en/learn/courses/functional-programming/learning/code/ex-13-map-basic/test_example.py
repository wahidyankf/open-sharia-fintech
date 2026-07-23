"""Example 13: pytest verification for map() Uppercases Every Word."""


def test_map_uppercases_every_element() -> None:
    words = ["a", "bee", "sea"]
    result = list(map(str.upper, words))
    assert result == ["A", "BEE", "SEA"]
    assert len(result) == len(words)  # => map never drops elements


# => Run: pytest -- Output: 1 passed
