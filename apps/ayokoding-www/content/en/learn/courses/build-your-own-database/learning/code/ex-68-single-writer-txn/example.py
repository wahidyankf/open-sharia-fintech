"""ex-68: single-writer-txn; exercises co-27."""

from __future__ import annotations


def demonstrate() -> dict[str, str]:
    """Return an observable fixture for this isolated exercise."""
    return {"example": "ex-68", "topic": "single-writer-txn", "concepts": "co-27"}


if __name__ == "__main__":
    print(demonstrate())
