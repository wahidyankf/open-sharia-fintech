"""Example 3: pytest verification for Structured Three Constructs."""

from example import classify_flagged, classify_structured


def test_structured_version_matches_flagged_version_for_all_cases() -> None:
    for n in (-10, -1, 0, 1, 10):  # => iteration over a spread of representative inputs
        assert classify_structured(n) == classify_flagged(n)  # => both must agree, always


def test_structured_version_uses_no_boolean_flag() -> None:
    import inspect  # => local import: only this test needs source inspection

    source = inspect.getsource(classify_structured)  # => read classify_structured's own source text
    assert "done" not in source  # => the AFTER version never declares a "goto flag" variable


# => Run: pytest -- Output: 2 passed
