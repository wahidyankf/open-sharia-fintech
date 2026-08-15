"""ex-20: pytest-cache-evict; exercises co-30, co-04."""

from __future__ import annotations


def demonstrate() -> dict[str, str]:
    """Return an observable fixture for this isolated exercise."""
    return {
        "example": "ex-20",
        "topic": "pytest-cache-evict",
        "concepts": "co-30, co-04",
    }


if __name__ == "__main__":
    print(demonstrate())
