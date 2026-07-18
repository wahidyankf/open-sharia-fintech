"""Example 4: pytest verification for Params Collected in Order."""

from example import Param, compile_two


def test_params_preserve_argument_order() -> None:
    sql, params = compile_two(Param(value="first"), Param(value="second"))
    assert sql == "?, ?"  # => two placeholders regardless of value content
    assert params == ["first", "second"]  # => first argument stays params[0]


def test_swapping_arguments_swaps_param_order() -> None:
    sql, params = compile_two(Param(value=1), Param(value=2))  # => 1 first this time
    assert params[0] == 1  # => order tracks argument position, not value
    sql2, params2 = compile_two(Param(value=2), Param(value=1))  # => 2 first now
    assert params2[0] == 2  # => flipping arguments flips params[0] too
    assert sql == sql2  # => the SQL SHAPE is identical either way -- only params differ


# => Run: pytest -- Output: 2 passed
