# pyright: strict
"""Example 41: Precision/Recall Direction (co-21)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic


def precision(retrieved: set[int], relevant: set[int]) -> float:  # => defines precision
    return (
        len(relevant & retrieved) / len(retrieved) if retrieved else 0.0
    )  # => returns len(relevant & retrieved) / len(retrieved) if retrieved e...


def recall(retrieved: set[int], relevant: set[int]) -> float:  # => defines recall
    return (
        len(relevant & retrieved) / len(relevant) if relevant else 0.0
    )  # => returns len(relevant & retrieved) / len(relevant) if relevant els...


def main() -> None:  # => defines main
    relevant: set[int] = {
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
    }  # => 10 documents are truly relevant

    cautious_retrieval: set[int] = {
        1
    }  # => co-21: retrieves ONLY 1 doc -- but it IS relevant
    p_cautious: float = precision(
        cautious_retrieval, relevant
    )  # => 1/1 -- perfect precision
    r_cautious: float = recall(
        cautious_retrieval, relevant
    )  # => 1/10 -- terrible recall
    print(
        f"cautious (retrieves 1 doc): precision={p_cautious:.4f}  recall={r_cautious:.4f}"
    )  # => shows cautious (retrieves 1 doc): precision=

    broad_retrieval: set[int] = set(
        range(1, 101)
    )  # => co-21: retrieves EVERYTHING from 1 to 100
    p_broad: float = precision(
        broad_retrieval, relevant
    )  # => 10/100 -- terrible precision
    r_broad: float = recall(broad_retrieval, relevant)  # => 10/10 -- perfect recall
    print(
        f"broad (retrieves 100 docs): precision={p_broad:.4f}  recall={r_broad:.4f}"
    )  # => shows broad (retrieves 100 docs): precision=

    assert p_cautious == 1.0 and r_cautious < 0.2, (
        "the cautious retrieval must have PERFECT precision, POOR recall"
    )  # => the cautious retrieval must have PERFECT precision, POOR recall
    assert r_broad == 1.0 and p_broad < 0.2, (
        "the broad retrieval must have PERFECT recall, POOR precision"
    )  # => the broad retrieval must have PERFECT recall, POOR precision
    print(
        "MATCH: retrieving 1 doc maximizes precision at recall's expense; retrieving everything does the reverse"
    )  # => shows MATCH: retrieving 1 doc maximizes precision at recall's expense; retrieving everything does the reverse


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
