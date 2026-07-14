"""Example 19: pytest verification for Name Mangling with a Double-Underscore Attribute."""

import pytest

from example import SecureBox


def test_direct_dunder_access_raises_attribute_error() -> None:
    box: SecureBox = SecureBox("1234")
    with pytest.raises(
        AttributeError
    ):  # => box.__pin does NOT exist under that literal name
        _ = box.__pin  # type: ignore  # => deliberately triggers the mangling gap this example teaches


def test_mangled_name_is_reachable() -> None:
    box: SecureBox = SecureBox("1234")
    assert box._SecureBox__pin == "1234"  # type: ignore  # => the actual, mangled attribute name (static checkers cannot resolve this literal spelling)


# => Run: pytest -- Output: 2 passed
