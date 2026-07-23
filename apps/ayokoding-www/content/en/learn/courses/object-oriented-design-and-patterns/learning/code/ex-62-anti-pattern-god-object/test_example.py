"""Example 62: pytest verification that the god-object smell is named and a fix sketched."""

from example import ApplicationManager, count_distinct_responsibilities, sketch_fix


def test_god_object_is_named_by_counting_distinct_responsibilities() -> None:
    assert count_distinct_responsibilities(ApplicationManager) == 3  # => auth + email + reporting, three concerns


def test_fix_is_sketched_with_one_line_per_extracted_responsibility() -> None:
    fix = sketch_fix()
    assert len(fix) == 3  # => one sketched service per responsibility identified above
    assert any("AuthService" in line for line in fix)  # => the auth split is named
    assert any("EmailService" in line for line in fix)  # => the email split is named
    assert any("ReportService" in line for line in fix)  # => the reporting split is named


# => Run: pytest -q -- Output: 2 passed
