"""Example 36: pytest verification for Bool Coercion on Load."""

from example import coerce_bool_on_load


def test_nonzero_int_coerces_to_true() -> None:
    assert coerce_bool_on_load(1) is True  # => the canonical "true" storage value


def test_zero_coerces_to_false() -> None:
    assert coerce_bool_on_load(0) is False  # => the canonical "false" storage value


def test_any_nonzero_int_still_coerces_to_true() -> None:
    assert coerce_bool_on_load(7) is True  # => SQLite never constrains this to exactly 0/1 -- coercion must too


# => Run: pytest -- Output: 3 passed
