"""Example 73: Interpret a Terminal Coverage Report -- Name the Uncovered Lines."""
# Only branch C (grade()'s fallback "C" return) is never exercised below -- the coverage
# report's own Missing column names the exact line, no debugger or guesswork required.

from grading import grade  # => co-27: the function whose branch coverage this file examines  # fmt: skip


def test_grade_a() -> None:  # => exercises branch A only  # fmt: skip
    assert grade(95) == "A"  # => a score comfortably inside the "A" range  # fmt: skip


def test_grade_b() -> None:  # => exercises branch B only -- branch C is NEVER called by this suite  # fmt: skip
    assert grade(75) == "B"  # => a score comfortably inside the "B" range  # fmt: skip
