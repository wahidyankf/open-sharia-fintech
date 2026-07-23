# learning/code/ex-07-assert-membership/test_example.py
"""Example 7: Assert Membership."""


# ex-07: membership assertions -- "is X inside this collection?" (co-03)
def supported_formats() -> list[str]:  # => the unit under test: a fixed list of formats
    return [
        "json",
        "xml",
        "csv",
    ]  # => a plain list -- membership uses Python's "in" operator


def test_membership_passes_for_a_present_element() -> None:  # => the "in" happy path
    formats = (
        supported_formats()
    )  # => arrange: call the function once, reuse the result
    assert "json" in formats  # => act+assert combined: "in" is itself the check (co-03)


def test_membership_for_an_absent_element() -> (
    None
):  # => the "not in" negation, its own test
    formats = (
        supported_formats()
    )  # => same arrange step, independent test (co-26 isolation)
    assert "yaml" not in formats  # => "not in" is membership's negation -- equally a plain assert  # fmt: skip
