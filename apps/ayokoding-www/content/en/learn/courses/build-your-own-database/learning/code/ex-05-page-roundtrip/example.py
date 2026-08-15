"""ex-05: page-roundtrip; exercises co-02, co-01."""

from __future__ import annotations


def demonstrate() -> dict[str, str]:
    """Return an observable fixture for this isolated exercise."""
    return {"example": "ex-05", "topic": "page-roundtrip", "concepts": "co-02, co-01"}


if __name__ == "__main__":
    print(demonstrate())
