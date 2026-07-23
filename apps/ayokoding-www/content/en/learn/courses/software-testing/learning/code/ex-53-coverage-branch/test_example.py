# learning/code/ex-53-coverage-branch/test_example.py
"""Example 53: Branch Coverage."""


# ex-53: --cov-branch tracks WHICH direction of an if/else actually ran, not just the line (co-21)  # fmt: skip
def classify(n: int) -> str:  # => the unit under test -- has TWO branches, only one tested below  # fmt: skip
    if n > 0:  # => this LINE runs either way -- but which BRANCH does it take?
        return "positive"  # => the branch this example's ONLY test actually takes
    else:  # => this branch is NEVER taken by the test below
        return "non-positive"  # => coverage --cov-branch reports THIS line as a missed branch  # fmt: skip


def test_classify_positive_only() -> None:  # => deliberately tests ONLY the positive case  # fmt: skip
    assert classify(5) == "positive"  # => the if-line executes, taking the TRUE branch only  # fmt: skip
    # => plain line coverage would call the "if n > 0:" line 100% covered (it DID run) --
    # => branch coverage additionally tracks that its FALSE outcome never happened (co-21)
