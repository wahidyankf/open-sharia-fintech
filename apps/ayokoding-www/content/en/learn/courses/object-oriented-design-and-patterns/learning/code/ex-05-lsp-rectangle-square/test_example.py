"""Example 5: pytest verification for Square(Rectangle) Breaks Liskov Substitution."""

from example import BrokenSquare, Rectangle, Square, resize_to_5_by_4


def test_broken_square_violates_the_rectangle_contract() -> None:
    # => this test DOCUMENTS the LSP violation: substitution changes behavior
    plain_area: float = resize_to_5_by_4(Rectangle(2.0, 2.0))
    broken_area: float = resize_to_5_by_4(BrokenSquare(2.0, 2.0))  # => substituted in
    assert plain_area == 20.0  # => the well-behaved base case
    assert broken_area == 16.0  # => NOT 20.0 -- proof the substitution broke the client
    assert plain_area != broken_area  # => the same client, two incompatible outcomes


def test_standalone_square_never_shares_rectangles_contract() -> None:
    square: Square = Square(4.0)  # => the fix: no inheritance relationship at all
    assert square.area() == 16.0  # => correct on Square's own terms
    assert not issubclass(Square, Rectangle)  # => structurally proves the two types are now unrelated


# => Run: pytest -- Output: 2 passed
