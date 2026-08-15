"""ex-77: pytest-recovery; exercises co-30, co-17."""

from __future__ import annotations


def demonstrate() -> dict[str, str]:
    """Return an observable fixture for this isolated exercise."""
    return {"example": "ex-77", "topic": "pytest-recovery", "concepts": "co-30, co-17"}


if __name__ == "__main__":
    print(demonstrate())
