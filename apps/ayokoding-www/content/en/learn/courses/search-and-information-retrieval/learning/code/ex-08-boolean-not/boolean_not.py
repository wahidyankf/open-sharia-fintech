# pyright: strict
"""Example 8: Boolean NOT (co-03)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic


def boolean_not(
    all_docs: list[int], postings: list[int]
) -> list[int]:  # => return every doc-id NOT present in postings -- a NOT query (co-03)
    """Return every doc-id NOT present in postings -- a NOT query (co-03)."""
    return sorted(
        set(all_docs) - set(postings)
    )  # => the full universe, minus this term's postings


def main() -> None:  # => defines main
    all_docs: list[int] = [0, 1, 2, 3, 4, 5]  # => every document id in the corpus
    deprecated_postings: list[int] = [1, 3]  # => docs containing the term "deprecated"
    result: list[int] = boolean_not(
        all_docs, deprecated_postings
    )  # => docs WITHOUT "deprecated"
    print(f"all docs: {all_docs}")  # => shows all docs
    print(
        f"'deprecated' postings: {deprecated_postings}"
    )  # => shows 'deprecated' postings
    print(f"NOT deprecated: {result}")  # => shows NOT deprecated

    for doc_id in deprecated_postings:  # => every excluded doc-id
        assert doc_id not in result, (
            f"doc {doc_id} contains 'deprecated' and must be excluded"
        )  # => doc {doc_id} contains 'deprecated' and must be excluded
    for doc_id in result:  # => every doc-id that DID survive
        assert doc_id not in deprecated_postings, (
            f"doc {doc_id} leaked into the NOT result"
        )  # => doc {doc_id} leaked into the NOT result
    print(
        f"MATCH: every doc in {deprecated_postings} is excluded, every other doc in {all_docs} survives"
    )  # => shows MATCH: every doc in


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
