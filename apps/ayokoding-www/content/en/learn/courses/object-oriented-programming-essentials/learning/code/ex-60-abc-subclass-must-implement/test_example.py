"""Example 60: pytest verification for An Incomplete Subclass Also Cannot Be Instantiated."""

import pytest

from example import Triangle


def test_subclass_missing_abstract_method_cannot_be_instantiated() -> None:
    with pytest.raises(TypeError):
        Triangle()  # type: ignore  # => area() was never implemented -- still abstract


# => Run: pytest -- Output: 1 passed
