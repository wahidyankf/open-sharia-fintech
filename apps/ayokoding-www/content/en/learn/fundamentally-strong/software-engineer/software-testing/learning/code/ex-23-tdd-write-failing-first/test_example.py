# learning/code/ex-23-tdd-write-failing-first/test_example.py
"""Example 23: TDD Step 1 -- Red."""

# ex-23: TDD step 1 -- RED. clamp() is called below but never defined anywhere in this file (co-17)


def test_clamp_restricts_value_to_a_range() -> None:
    # => act: calls a function that does not exist yet anywhere in this module or an import
    result = clamp(15, minimum=0, maximum=10)  # => NameError: 'clamp' is not defined  # fmt: skip
    # => this line is UNREACHABLE right now -- pytest reports the NameError from the line
    # => above as the test's failure, before this assert is ever evaluated at all
    assert (
        result == 10
    )  # => the eventual, INTENDED behavior -- not yet true, not yet checked
