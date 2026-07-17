"""Example 55: pytest verification for map2 Combines Two Options."""

from example import Nothing, Some, add, map2


def test_map2_combines_when_both_present_and_short_circuits_otherwise() -> None:
    assert map2(add, Some(2), Some(3)) == Some(5)
    assert map2(add, Some(2), Nothing()) == Nothing()
    assert map2(add, Nothing(), Some(3)) == Nothing()


# => Run: pytest -- Output: 1 passed
