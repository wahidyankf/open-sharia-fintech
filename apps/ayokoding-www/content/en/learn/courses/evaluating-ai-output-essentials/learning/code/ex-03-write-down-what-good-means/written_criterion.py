# learning/code/ex-03-write-down-what-good-means/written_criterion.py
"""Worked Example 3: Write Down What Good Means."""  # => co-02: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

ANSWER = "Nimbus accounts start on the Free plan with 15 GB of storage included."  # => co-02: the candidate output under review


def grader_vague(answer: str) -> bool:  # => co-02: "make it better" -- an unwritten, personal sense of quality
    """A stand-in for one reviewer's un-articulated gut feeling."""  # => co-02: documents grader_vague's contract -- no runtime output, just sets its __doc__
    return len(answer) > 20 and "Nimbus" in answer  # => co-02: reviewer A's private, never-written-down bar


def grader_vague_second_reviewer(answer: str) -> bool:  # => co-02: a SECOND reviewer applying the same unwritten instruction
    """A different reviewer's own un-articulated gut feeling for the same vague instruction."""  # => co-02: documents grader_vague_second_reviewer's contract -- no runtime output, just sets its __doc__
    return "storage" in answer and "GB" in answer and "plan" in answer.lower()  # => co-02: reviewer B's DIFFERENT private bar


def written_criterion_reader_a(answer: str) -> tuple[bool, str]:  # => co-02: reader A's OWN implementation of the written spec
    """Reader A's independent implementation of: 'names the plan AND its exact storage amount.'"""  # => co-02: documents written_criterion_reader_a's contract -- no runtime output, just sets its __doc__
    has_plan_name = "Free plan" in answer  # => co-02: requirement 1, made explicit and checkable
    has_storage_amount = "15 GB" in answer  # => co-02: requirement 2, made explicit and checkable
    passed = has_plan_name and has_storage_amount  # => co-02: BOTH requirements, not "some vague sense of completeness"
    reason = f"plan named: {has_plan_name}, storage amount stated: {has_storage_amount}"  # => co-02: a reason anyone can re-check by eye
    return passed, reason  # => co-02: returns this computed value to the caller


def written_criterion_reader_b(answer: str) -> tuple[bool, str]:  # => co-02: reader B's OWN, independently-coded implementation
    """Reader B's independent implementation of the SAME written spec, coded without seeing reader A's."""  # => co-02: documents written_criterion_reader_b's contract -- no runtime output, just sets its __doc__
    checks = {"Free plan" in answer, "15 GB" in answer}  # => co-02: same two requirements, expressed as a set instead of two names
    passed = checks == {True}  # => co-02: passes only when BOTH requirements independently evaluate True
    reason = f"both requirements met: {passed}"  # => co-02: a differently-worded but equivalent reason
    return passed, reason  # => co-02: returns this computed value to the caller


if __name__ == "__main__":  # => co-02: entry point -- runs only when this file executes directly, not on import
    vague_a = grader_vague(ANSWER)  # => co-02: reviewer A's vague verdict
    vague_b = grader_vague_second_reviewer(ANSWER)  # => co-02: reviewer B's vague verdict, same instruction
    print(f"Reviewer A (vague): {vague_a} | Reviewer B (vague): {vague_b}")  # => co-02: prints both private verdicts
    a_passed, a_reason = written_criterion_reader_a(ANSWER)  # => co-02: reader A applies the WRITTEN criterion
    b_passed, b_reason = written_criterion_reader_b(ANSWER)  # => co-02: reader B applies the SAME written criterion
    print(f"Reader A (written): {a_passed} ({a_reason})")  # => co-02: prints reader A's reproducible verdict + reason
    print(f"Reader B (written): {b_passed} ({b_reason})")  # => co-02: prints reader B's independently-coded verdict
    assert a_passed == b_passed, "two readers applying the SAME written criterion must reach the SAME verdict"  # => co-02
    print(f"Verdicts match: {a_passed == b_passed}")  # => co-02: the point of ex-03 -- reproducibility, not agreement by luck
    # => co-02: a criterion two people apply identically is the minimum working unit of an eval
