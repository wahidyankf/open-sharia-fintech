"""Example 23: pytest verification for compile() Purity."""

from example import Select


def test_repeated_compile_calls_return_equal_but_distinct_lists() -> None:
    query = Select(table="orders").where_id(3)  # => built once
    sql_a, params_a = query.compile()  # => first call
    sql_b, params_b = query.compile()  # => second call, same instance
    assert (sql_a, params_a) == (sql_b, params_b)  # => equal content
    assert params_a is not params_b  # => but distinct list objects -- no shared mutable state


def test_mutating_a_returned_params_list_does_not_leak() -> None:
    query = Select(table="orders").where_id(3)  # => built once
    _, params = query.compile()  # => grab the returned list
    params.append(999)  # => mutate the CALLER's copy
    _, fresh_params = query.compile()  # => compile again, from the SAME unmutated query
    assert fresh_params == [3]  # => the mutation never reached query's own state


# => Run: pytest -- Output: 2 passed
