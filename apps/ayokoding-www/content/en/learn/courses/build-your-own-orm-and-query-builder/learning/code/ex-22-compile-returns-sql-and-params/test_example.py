"""Example 22: pytest verification for compile() Returns a Tuple."""

from example import Eq, Select


def test_compile_returns_exactly_two_elements() -> None:
    result = Select(table="t").compile()  # => no clauses at all -- still a tuple
    assert isinstance(result, tuple) and len(result) == 2  # => always 2 elements


def test_compile_shape_is_stable_across_clause_combinations() -> None:
    bare = Select(table="t").compile()  # => zero clauses
    with_where = Select(table="t").where(Eq(column="x", value=1)).compile()  # => one clause
    assert len(bare) == len(with_where) == 2  # => the SHAPE never changes, only the contents


# => Run: pytest -- Output: 2 passed
