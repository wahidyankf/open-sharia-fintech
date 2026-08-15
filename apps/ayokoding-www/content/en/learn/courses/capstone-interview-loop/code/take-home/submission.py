"""A small, standard-library-only submission checklist used by the take-home artifact."""

from collections.abc import Collection


REQUIRED_FILES = frozenset({"README.md", "test_submission.py"})


def missing_review_basics(files: Collection[str]) -> list[str]:
    """List the reviewer-facing basics absent from a scoped Python submission."""
    return sorted(REQUIRED_FILES.difference(files))


def is_clean_checkout_ready(files: Collection[str]) -> bool:
    """Require a README, a focused test, and one non-test Python implementation file."""
    has_implementation = any(
        name.endswith(".py") and not name.startswith("test_") for name in files
    )
    return not missing_review_basics(files) and has_implementation
