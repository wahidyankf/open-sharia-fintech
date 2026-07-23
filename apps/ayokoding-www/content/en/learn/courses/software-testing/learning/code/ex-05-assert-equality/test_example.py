# learning/code/ex-05-assert-equality/test_example.py
"""Example 5: Assert Equality."""


# ex-05: equality assertions -- the most common assertion shape in any test suite (co-03)
def to_upper(text: str) -> str:  # => the unit under test
    return (
        text.upper()
    )  # => stdlib str.upper -- deterministic, no locale surprises here


def test_equality_passes_on_a_match() -> (
    None
):  # => the "happy path" half of this example
    assert to_upper("hello") == "HELLO"  # => == compares by VALUE, not identity (co-03)


def test_equality_fails_on_a_mismatch() -> None:  # => proves == genuinely discriminates
    assert (
        to_upper("hello") != "hello"
    )  # => != is equality's negation -- also a plain assert
    # => this line is deliberately the OPPOSITE assertion (!=) so the test itself passes
    # => while still demonstrating that a naive equality check would have failed here
