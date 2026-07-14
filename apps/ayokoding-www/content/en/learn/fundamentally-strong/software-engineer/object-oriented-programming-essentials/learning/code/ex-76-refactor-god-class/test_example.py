"""Example 76: pytest verification for Splitting a Two-Responsibility Class into Collaborators."""

from example import Formatter, ReportGenerator, Sender


def test_each_collaborator_has_exactly_one_responsibility() -> None:
    assert Formatter().format("x") == "[REPORT] x"  # => formatting, and only formatting
    assert Sender().send("y") == "sent: y"  # => sending, and only sending


def test_report_generator_still_produces_the_original_behavior() -> None:
    generator: ReportGenerator = ReportGenerator()
    assert generator.send_report("Q3 numbers") == "sent: [REPORT] Q3 numbers"


# => Run: pytest -- Output: 2 passed
