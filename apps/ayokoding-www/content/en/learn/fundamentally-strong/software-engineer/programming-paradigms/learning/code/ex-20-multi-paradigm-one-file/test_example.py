"""Example 20: pytest verification for Multi-Paradigm One File."""

from example import LineItem, even_squares


def test_the_oo_class_computes_its_own_subtotal() -> None:
    item = LineItem(price=100, qty=2)  # => construct via the dataclass
    assert item.subtotal() == 200  # => state and behavior bundled on the object


def test_the_comprehension_and_generator_agree_on_values() -> None:
    items = [LineItem(10, 1), LineItem(20, 2)]  # => two OO objects
    subtotals = [item.subtotal() for item in items]  # => a comprehension over OO objects
    assert subtotals == [10, 40]  # => 10*1, 20*2

    squares = list(even_squares(6))  # => draining the generator runs it
    assert squares == [0, 4, 16]  # => 0^2, 2^2, 4^2 for the even numbers below 6


# => Run: pytest -- Output: 2 passed
