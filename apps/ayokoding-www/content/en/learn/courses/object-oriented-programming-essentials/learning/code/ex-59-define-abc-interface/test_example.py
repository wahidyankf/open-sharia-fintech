"""Example 59: pytest verification for Define an ABC Interface."""

import pytest

from example import Shape


def test_abc_with_unimplemented_method_cannot_be_instantiated() -> None:
    with pytest.raises(TypeError):  # => Shape() must raise, never silently construct
        Shape()  # type: ignore  # => deliberately triggers the ABC instantiation guard


# => Run: pytest -- Output: 1 passed
