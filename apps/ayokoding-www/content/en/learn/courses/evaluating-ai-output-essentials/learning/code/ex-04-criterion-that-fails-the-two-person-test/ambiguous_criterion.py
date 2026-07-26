# learning/code/ex-04-criterion-that-fails-the-two-person-test/ambiguous_criterion.py
"""Worked Example 4: A Criterion That Fails the Two-Person Test."""  # => co-02: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

ANSWER = "Nimbus is a solid choice if you want reliable cloud storage with strong security."  # => co-02: the candidate output under review


def sounds_helpful_reader_1(answer: str) -> bool:  # => co-02: reader 1 applying "the answer should sound helpful"
    """Reader 1's interpretation: helpful means confident and positive in tone."""  # => co-02: documents sounds_helpful_reader_1's contract -- no runtime output, just sets its __doc__
    positive_words = ("solid", "reliable", "strong")  # => co-02: reader 1's private notion of "sounds helpful"
    return any(word in answer for word in positive_words)  # => co-02: reader 1 says True -- the tone reads confident


def sounds_helpful_reader_2(answer: str) -> bool:  # => co-02: reader 2 applying the SAME instruction, differently
    """Reader 2's interpretation: helpful means it actually answers a concrete question."""  # => co-02: documents sounds_helpful_reader_2's contract -- no runtime output, just sets its __doc__
    concrete_markers = ("GB", "$", "plan", "step")  # => co-02: reader 2's private notion of "sounds helpful"
    return any(marker in answer for marker in concrete_markers)  # => co-02: reader 2 says False -- no concrete detail at all


def names_a_concrete_fact(answer: str) -> tuple[bool, str]:  # => co-02: the rewrite -- swaps "sounds helpful" for something checkable
    """Pass iff the answer states at least one concrete, checkable Nimbus fact (a plan name or a GB figure)."""  # => co-02: documents names_a_concrete_fact's contract -- no runtime output, just sets its __doc__
    has_plan = "plan" in answer.lower()  # => co-02: requirement candidate 1 -- names a specific plan
    has_gb_figure = "GB" in answer  # => co-02: requirement candidate 2 -- names a specific storage figure
    passed = has_plan or has_gb_figure  # => co-02: EITHER concrete fact satisfies the rewritten criterion
    reason = f"plan named: {has_plan}, GB figure named: {has_gb_figure}"  # => co-02: a reason both readers can verify identically
    return passed, reason  # => co-02: returns this computed value to the caller


if __name__ == "__main__":  # => co-02: entry point -- runs only when this file executes directly, not on import
    r1 = sounds_helpful_reader_1(ANSWER)  # => co-02: reader 1's verdict on the ambiguous instruction
    r2 = sounds_helpful_reader_2(ANSWER)  # => co-02: reader 2's verdict on the SAME ambiguous instruction
    print(f"Reader 1 ('sounds helpful'): {r1} | Reader 2 ('sounds helpful'): {r2}")  # => co-02: prints the disagreement
    assert r1 != r2, "the ambiguous criterion must produce disagreement for this demo to make its point"  # => co-02
    fixed_passed, fixed_reason = names_a_concrete_fact(ANSWER)  # => co-02: both readers apply the SAME rewritten rule
    print(f"Rewritten criterion (both readers): {fixed_passed} ({fixed_reason})")  # => co-02: one shared, reproducible verdict
    assert fixed_passed is False, "this ANSWER names no concrete fact -- both readers must now agree it fails"  # => co-02
    print("Disagreement disappeared: both readers now apply the identical, written rule")  # => co-02: the point of ex-04
    # => co-02: an ambiguous criterion is not yet an eval -- it is still two people's opinions in disguise
