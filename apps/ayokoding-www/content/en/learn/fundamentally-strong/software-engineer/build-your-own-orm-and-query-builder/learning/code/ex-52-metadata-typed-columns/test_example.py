"""Example 52: pytest verification for Metadata-Typed Column Coercion."""

from example import Column, coerce_by_column_type


def test_bool_typed_column_routes_to_the_bool_coercer() -> None:
    column = Column(name="enabled", python_type=bool)  # => a bool-typed column
    assert coerce_by_column_type(column, 1) is True  # => nonzero coerces to True
    assert coerce_by_column_type(column, 0) is False  # => zero coerces to False


def test_str_typed_column_routes_to_the_str_coercer() -> None:
    column = Column(name="label", python_type=str)  # => a str-typed column
    assert coerce_by_column_type(column, "hello") == "hello"  # => TEXT passes through unchanged


# => Run: pytest -- Output: 2 passed
