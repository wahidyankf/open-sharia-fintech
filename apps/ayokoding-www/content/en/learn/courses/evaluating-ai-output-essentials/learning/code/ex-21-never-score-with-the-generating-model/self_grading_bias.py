# learning/code/ex-21-never-score-with-the-generating-model/self_grading_bias.py
"""Worked Example 21: Never Score With the Generating Model."""  # => co-12: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

FLAWED_ANSWER = "Nimbus Pro includes 20 GB of storage, ready whenever you need it."  # => co-05: confidently wrong -- 200 GB is correct
KEY_FACT = "200 GB"  # => co-04: the fact that actually matters, independent of tone


def same_system_self_grade(answer: str) -> bool:  # => co-12: stands in for asking the SAME system that wrote the answer to grade it
    """A mocked 'self-grade' -- the same system that produced FLAWED_ANSWER judging its own fluent tone."""  # => co-12: documents same_system_self_grade's contract -- no runtime output, just sets its __doc__
    sounds_confident = "ready" in answer or "includes" in answer  # => co-12: judges TONE, the exact thing it optimized for
    return sounds_confident  # => co-12: the system's own stylistic habits make its own mistakes look fine to itself


def independent_deterministic_scorer(answer: str, required_fact: str) -> bool:  # => co-12: a scorer with NO stake in the answer
    """An independent, deterministic check with no relationship to whatever produced `answer`."""  # => co-12: documents independent_deterministic_scorer's contract -- no runtime output, just sets its __doc__
    return required_fact in answer  # => co-12: checks the fact, never the fluency


if __name__ == "__main__":  # => co-12: entry point -- runs only when this file executes directly, not on import
    self_grade_result = same_system_self_grade(FLAWED_ANSWER)  # => co-12: the biased verdict
    independent_result = independent_deterministic_scorer(FLAWED_ANSWER, KEY_FACT)  # => co-12: the unbiased verdict
    print(f"Self-grade (same system): {self_grade_result}")  # => co-12: prints the biased, falsely-positive verdict
    print(f"Independent deterministic scorer: {independent_result}")  # => co-12: prints the correct, negative verdict
    assert self_grade_result is True, "a same-system self-grade must wrongly approve its own fluent, wrong answer"  # => co-12
    assert independent_result is False, "an independent, fact-based scorer must catch the same error"  # => co-12
    print("MATCH: the system that made the mistake shares the same blind spot that produced it")  # => co-12
    # => co-12: judging whether a SUBJECTIVE score is trustworthy needs measured agreement -- that machinery belongs
    # => co-12: to evaluating-ai-systems-in-depth, not here; this course stops at deterministic, independent scorers
