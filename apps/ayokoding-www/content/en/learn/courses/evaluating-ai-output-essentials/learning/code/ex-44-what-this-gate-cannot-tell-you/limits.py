# learning/code/ex-44-what-this-gate-cannot-tell-you/limits.py
"""Worked Example 44: What This Gate Cannot Tell You."""  # => co-12: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from typing import NamedTuple  # => co-12: a typed record for one honest limit of this course's light gate


class Limit(NamedTuple):  # => co-12: one thing this gate provably cannot answer
    question_this_gate_cannot_answer: str  # => co-12: the exact question a pass rate alone cannot settle
    owning_deep_course_concept: str  # => co-12: which evaluating-ai-systems-in-depth concept owns the answer


GATE_LIMITS = [  # => co-12: exactly three honest limits -- not an exhaustive list, but the three this course names
    Limit(  # => co-12: limit 1
        "WHY did this case fail -- what specific failure pattern caused it?",  # => co-12: the pass/fail bit alone never says why
        "error analysis (systematic failure-mode categorization)",  # => co-12: the deep course's owning concept
    ),  # => co-12: closes limit 1
    Limit(  # => co-12: limit 2
        "Is a SUBJECTIVE quality (tone, faithfulness, helpfulness) actually being scored correctly?",  # => co-12
        "LLM-as-judge with measured human agreement",  # => co-12: the deep course's owning concept
    ),  # => co-12: closes limit 2
    Limit(  # => co-12: limit 3
        "Can this gate be trusted to block a bad merge automatically, unattended?",  # => co-12: a ten-case gate is a manual check
        "CI gating with judge reliability guarantees",  # => co-12: the deep course's owning concept
    ),  # => co-12: closes limit 3
]  # => co-12: closes GATE_LIMITS


if __name__ == "__main__":  # => co-12: entry point -- runs only when this file executes directly, not on import
    print(f"This gate cannot answer {len(GATE_LIMITS)} kinds of question:")  # => co-12: states the count up front
    for limit in GATE_LIMITS:  # => co-12: one printed line per documented limit
        print(f"  - {limit.question_this_gate_cannot_answer}")  # => co-12: prints the unanswerable question
        print(f"    -> owned by: {limit.owning_deep_course_concept}")  # => co-12: prints where the answer actually lives
    assert len(GATE_LIMITS) == 3, "this course names exactly three honest limits, not an exhaustive list"  # => co-12
    assert all("deep" not in limit.owning_deep_course_concept for limit in GATE_LIMITS), "concept names must be self-contained"  # => co-12
    print("MATCH: every limit maps to a NAMED concept in the deep course, not a vague 'do more evals' gesture")  # => co-12
    # => co-12: recognising this boundary -- not crossing it -- is what evaluating-ai-output-essentials teaches you to do
