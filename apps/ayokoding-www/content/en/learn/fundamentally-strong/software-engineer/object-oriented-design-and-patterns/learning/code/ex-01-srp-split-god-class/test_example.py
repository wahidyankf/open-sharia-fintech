"""Example 1: pytest verification for Split a God Class by Responsibility."""

from example import DataParser, ReportFormatter, ReportWriter


def test_each_class_carries_only_its_own_responsibility() -> None:
    # => structural check: no class exposes a method belonging to another concern
    # => DataParser must never format or save -- parsing is its one reason to change
    assert not hasattr(DataParser, "format") and not hasattr(DataParser, "save")
    # => ReportFormatter must never parse or save -- formatting is its one job
    assert not hasattr(ReportFormatter, "parse") and not hasattr(ReportFormatter, "save")
    # => ReportWriter must never parse or format -- persistence is its one job
    assert not hasattr(ReportWriter, "parse") and not hasattr(ReportWriter, "format")


def test_pipeline_produces_expected_report() -> None:
    # => three collaborators, each doing exactly one step of the pipeline
    rows: list[str] = DataParser().parse("alice\n\nbob\ncarol\n")  # => rows is ["alice", "bob", "carol"]
    report: str = ReportFormatter().format(rows)  # => formats the parsed rows
    sink: list[str] = []  # => the in-memory "file" ReportWriter appends to
    ReportWriter().save(report, sink)  # => the only mutation of sink in this test
    assert sink == ["- alice\n- bob\n- carol"]  # => exactly one save recorded


# => Run: pytest -- Output: 2 passed
