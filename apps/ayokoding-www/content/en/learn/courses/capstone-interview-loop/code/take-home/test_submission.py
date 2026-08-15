from submission import is_clean_checkout_ready, missing_review_basics


def test_reports_missing_reviewer_basics() -> None:
    assert missing_review_basics({"submission.py"}) == [
        "README.md",
        "test_submission.py",
    ]


def test_accepts_a_small_clean_checkout_shape() -> None:
    assert is_clean_checkout_ready({"README.md", "submission.py", "test_submission.py"})
    assert not is_clean_checkout_ready({"README.md", "test_submission.py"})
