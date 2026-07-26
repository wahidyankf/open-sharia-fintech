# learning/code/ex-13-substring-scorer/substring_scorer.py
"""Worked Example 13: Substring Scorer."""  # => co-05: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic


def substring_scorer(output: str, required_fact: str) -> bool:  # => co-05: for free-text answers, not just single-token ones
    """Pass iff `required_fact` appears verbatim anywhere inside `output`."""  # => co-05: documents substring_scorer's contract -- no runtime output, just sets its __doc__
    return required_fact in output  # => co-05: no position requirement -- the fact just has to be present somewhere


if __name__ == "__main__":  # => co-05: entry point -- runs only when this file executes directly, not on import
    required_fact = "15 GB"  # => co-04: case-01's required fact from the co-03 dataset
    complete_answer = "New Nimbus accounts start with 15 GB of free storage to use right away."  # => co-05: the fact is present
    incomplete_answer = "New Nimbus accounts start with a generous amount of free storage."  # => co-05: the fact is MISSING
    complete_result = substring_scorer(complete_answer, required_fact)  # => co-05: the pass path
    incomplete_result = substring_scorer(incomplete_answer, required_fact)  # => co-05: the fail path
    print(f"substring_scorer(complete, {required_fact!r}) = {complete_result}")  # => co-05: prints the pass verdict
    print(f"substring_scorer(incomplete, {required_fact!r}) = {incomplete_result}")  # => co-05: prints the fail verdict
    assert complete_result is True, "the fact's presence, anywhere, must pass"  # => co-05: confirms the pass path
    assert incomplete_result is False, "a vague paraphrase missing the fact must fail"  # => co-05: confirms the fail path
    print("MATCH: substring scoring tolerates free-text phrasing as long as the required fact survives")  # => co-05
    # => co-05: substring scoring is the workhorse for "did the answer keep the one fact that matters" cases
