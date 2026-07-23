"""Example 26: pytest verification for Structured Guard Clauses."""

from example import discount_guarded, discount_nested


def test_guarded_version_matches_nested_version_for_every_combination() -> None:
    for is_member in (True, False):  # => exhaustive sweep over both booleans
        for total in (0, 50, 100, 101, 200):  # => a spread including the exact boundary value 100
            for has_coupon in (True, False):  # => and both coupon states
                assert discount_nested(is_member, total, has_coupon) == discount_guarded(is_member, total, has_coupon)  # => must agree on every single combination


def test_guarded_version_has_no_nested_if_inside_if() -> None:
    import inspect  # => local import: only this test needs source inspection

    source = inspect.getsource(discount_guarded)  # => read the guarded function's own source
    # => count leading-whitespace "if" lines that start deeper than one indent level (4 spaces)
    deeply_nested = [line for line in source.splitlines() if line.strip().startswith("if ") and line.startswith("        if")]
    assert deeply_nested == []  # => no guard clause is nested inside another guard clause


# => Run: pytest -- Output: 2 passed
