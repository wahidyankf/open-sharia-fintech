# learning/code/ex-20-a-scorer-that-lies/scorer_that_lies.py
"""Worked Example 20: A Scorer That Lies."""  # => co-02: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

WRONG_ANSWER = "Nimbus Pro includes 20 GB of storage, plenty for most teams."  # => co-05: a confidently, factually WRONG answer


def loose_scorer(output: str) -> bool:  # => co-05: an over-permissive scorer -- checks for "GB", not the actual number
    """Pass iff the output merely mentions a GB figure at all -- too loose to catch a wrong number."""  # => co-05: documents loose_scorer's contract -- no runtime output, just sets its __doc__
    return "GB" in output  # => co-05: satisfied by ANY GB figure, right or wrong


def tightened_scorer(output: str, expected_value: str) -> bool:  # => co-05: the fix -- check the SPECIFIC expected figure
    """Pass iff the output contains the specific expected GB figure, not merely any GB figure."""  # => co-05: documents tightened_scorer's contract -- no runtime output, just sets its __doc__
    return expected_value in output  # => co-05: the exact fact, not just its unit


if __name__ == "__main__":  # => co-05: entry point -- runs only when this file executes directly, not on import
    loose_result = loose_scorer(WRONG_ANSWER)  # => co-05: the over-permissive scorer's verdict on a WRONG answer
    print(f"loose_scorer(WRONG_ANSWER) = {loose_result}")  # => co-05: prints the false pass
    assert loose_result is True, "the loose scorer must wrongly pass this factually incorrect answer"  # => co-05: proves the lie

    tightened_result = tightened_scorer(WRONG_ANSWER, expected_value="200 GB")  # => co-05: the tightened scorer's verdict
    print(f"tightened_scorer(WRONG_ANSWER, '200 GB') = {tightened_result}")  # => co-05: prints the corrected fail
    assert tightened_result is False, "the tightened scorer must catch the wrong figure"  # => co-05: confirms the fix

    correct_answer = "Nimbus Pro includes 200 GB of storage."  # => co-05: what a genuinely correct answer looks like
    correct_result = tightened_scorer(correct_answer, expected_value="200 GB")  # => co-05: the tightened scorer on a right answer
    print(f"tightened_scorer(correct_answer, '200 GB') = {correct_result}")  # => co-05: prints the still-passing correct case
    assert correct_result is True, "the tightened scorer must still pass a genuinely correct answer"  # => co-05
    print("MATCH: a scorer that passes ANY plausible-looking output is worse than no eval at all -- it hides the bug")  # => co-05
    # => co-05: a green eval run built on a lying scorer is more dangerous than no eval, because it manufactures false confidence
