# learning/code/ex-39-regression-case-from-a-bug-report/regression_case.py
"""Worked Example 39: A Regression Case from a Bug Report."""  # => co-10: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

BUG_REPORT = (  # => co-10: a real user report, quoted verbatim -- the seed of a new permanent case
    "A user asked 'Can I share a Nimbus file with someone outside my team?' and the system answered "  # => co-10: part 1
    "'No, sharing is restricted to your own team,' which is WRONG -- external sharing is allowed via link."  # => co-10: part 2
)  # => co-10: closes BUG_REPORT
NEW_CASE = {  # => co-10: the bug report, turned into a permanent, checkable case
    "id": "case-13",  # => co-10: the next available case id -- this case now lives in the dataset forever
    "input": "Can I share a Nimbus file with someone outside my team?",  # => co-10: the exact question that broke
    "expected": "link",  # => co-10: the fact the correct answer must contain
    "criterion": "answer must confirm external sharing is possible via a share link",  # => co-10: written down, per co-02
}  # => co-10: closes NEW_CASE


def answer_pre_fix(question: str) -> str:  # => co-10: the system's behavior BEFORE the bug is fixed
    del question  # => co-10: this mock ignores its input -- it always gives the same wrong answer, matching the bug report
    return "No, sharing is restricted to your own team."  # => co-10: reproduces the exact reported bug


def answer_post_fix(question: str) -> str:  # => co-10: the system's behavior AFTER the bug is fixed
    del question  # => co-10: this mock ignores its input -- it always gives the corrected answer
    return "Yes -- share a file outside your team using a share link."  # => co-10: the corrected behavior


if __name__ == "__main__":  # => co-10: entry point -- runs only when this file executes directly, not on import
    print(f"Bug report: {BUG_REPORT}")  # => co-10: prints the original report this case is sourced from
    pre_fix_output = answer_pre_fix(NEW_CASE["input"])  # => co-10: run the NEW case against the pre-fix system
    pre_fix_passes = NEW_CASE["expected"] in pre_fix_output  # => co-10: does the pre-fix output contain the required fact?
    print(f"Pre-fix output: {pre_fix_output!r} -> passes: {pre_fix_passes}")  # => co-10: prints the pre-fix verdict
    assert pre_fix_passes is False, "the regression case must FAIL against the pre-fix system -- it reproduces the bug"  # => co-10

    post_fix_output = answer_post_fix(NEW_CASE["input"])  # => co-10: run the SAME case against the post-fix system
    post_fix_passes = NEW_CASE["expected"] in post_fix_output  # => co-10: does the post-fix output contain the required fact?
    print(f"Post-fix output: {post_fix_output!r} -> passes: {post_fix_passes}")  # => co-10: prints the post-fix verdict
    assert post_fix_passes is True, "the regression case must PASS against the post-fix system"  # => co-10
    print("MATCH: case-13 now guards this exact bug forever -- any future prompt change that reintroduces it will be caught")  # => co-10
    # => co-10: every failure a human reports becomes a permanent case -- this is how the dataset earns its coverage
