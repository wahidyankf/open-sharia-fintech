"""Example 31: pytest verification for A Property Backed by a Private Field."""

from example import Rectangle


def test_external_code_reads_through_public_property() -> None:
    r: Rectangle = Rectangle(5.0)
    assert r.width == 5.0  # => callers use .width, never ._width, by convention
    assert r._width == 5.0  # => the private field genuinely backs the property


# => Run: pytest -- Output: 1 passed
