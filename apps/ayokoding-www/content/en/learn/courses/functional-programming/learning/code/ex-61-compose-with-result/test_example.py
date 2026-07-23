"""Example 61: pytest verification for Composing Result-Returning Functions."""

from example import Err, Ok, kleisli_compose, parse_int, reciprocal


def test_composed_pipeline_propagates_the_first_failure() -> None:
    pipeline = kleisli_compose(parse_int, reciprocal)
    assert pipeline("1") == Ok(1)
    assert pipeline("bad") == Err("'bad' is not an integer")
    assert pipeline("0") == Err("cannot take the reciprocal of zero")


# => Run: pytest -- Output: 1 passed
