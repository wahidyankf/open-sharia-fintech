"""ex-50: pytest-lsm-compaction; exercises co-30, co-13."""

from __future__ import annotations


def demonstrate() -> dict[str, str]:
    """Return an observable fixture for this isolated exercise."""
    return {
        "example": "ex-50",
        "topic": "pytest-lsm-compaction",
        "concepts": "co-30, co-13",
    }


if __name__ == "__main__":
    print(demonstrate())
