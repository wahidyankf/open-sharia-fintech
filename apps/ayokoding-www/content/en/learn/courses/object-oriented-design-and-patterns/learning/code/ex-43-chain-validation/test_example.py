"""Example 43: pytest verification for the Validation Pipeline as a Handler Chain."""

from example import AlphaOnlyRule, MinLengthRule, NotEmptyRule


def _build_pipeline() -> NotEmptyRule:
    not_empty, min_length, alpha_only = NotEmptyRule(), MinLengthRule(), AlphaOnlyRule()
    not_empty.set_next(min_length).set_next(alpha_only)
    return not_empty


def test_first_failure_stops_the_chain_and_reports_that_error() -> None:
    assert _build_pipeline().validate("") == "value must not be empty"  # => rule 1 fails first


def test_second_rule_only_runs_once_the_first_rule_passes() -> None:
    assert _build_pipeline().validate("ab") == "value must be at least 4 characters"  # => rule 1 passed, rule 2 caught it


def test_value_passing_every_rule_returns_none() -> None:
    assert _build_pipeline().validate("abcd") is None  # => every rule in the chain passed


# => Run: pytest -- Output: 3 passed
