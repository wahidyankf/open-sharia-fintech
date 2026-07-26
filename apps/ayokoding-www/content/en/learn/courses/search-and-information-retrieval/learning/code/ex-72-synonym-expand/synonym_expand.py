# pyright: strict
"""Example 72: Synonym Expand (co-34)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic


def expand_query(
    query_terms: list[str], synonyms: dict[str, set[str]]
) -> set[str]:  # => expand every query term into itself PLUS all of its known synonyms
    """Expand every query term into itself PLUS all of its known synonyms."""
    expanded: set[str] = (
        set()
    )  # => co-34: the query terms, UNIONED with every synonym they map to
    for term in query_terms:  # => iterates one item at a time
        expanded.add(term)  # => the ORIGINAL term always stays in the expanded set
        expanded |= synonyms.get(
            term, set()
        )  # => co-34: plus every synonym registered for it
    return expanded  # => returns expanded


def execute_or_query(
    index: dict[str, set[int]], terms: set[str]
) -> set[
    int
]:  # => boolean OR over an arbitrary set of terms -- any document matching any term qualifies
    """Boolean OR over an arbitrary set of terms -- any document matching any term qualifies."""
    hits: set[int] = set()  # => hits = set()
    for term in terms:  # => iterates one item at a time
        hits |= index.get(term, set())  # => co-07: co-07's own boolean OR merge
    return hits  # => returns hits


def main() -> None:  # => defines main
    synonyms: dict[str, set[str]] = {
        "car": {"automobile", "vehicle"}
    }  # => co-34: "car" expands to include these
    index: dict[
        str, set[int]
    ] = {  # => a small inverted index -- doc 1 uses ONLY the synonym, never "car" itself
        "car": {0},  # => entry for 'car'
        "automobile": {1},  # => entry for 'automobile'
        "bicycle": {2},  # => entry for 'bicycle'
    }  # => opens/closes this multi-line literal

    literal_hits: set[int] = execute_or_query(
        index, {"car"}
    )  # => co-34: WITHOUT synonym expansion
    expanded_terms: set[str] = expand_query(
        ["car"], synonyms
    )  # => co-34: "car" expanded to {"car", "automobile", "vehicle"}
    expanded_hits: set[int] = execute_or_query(
        index, expanded_terms
    )  # => co-34: WITH synonym expansion
    print(
        f"literal query 'car': {sorted(literal_hits)}"
    )  # => shows literal query 'car'
    print(f"expanded terms: {sorted(expanded_terms)}")  # => shows expanded terms
    print(f"expanded query: {sorted(expanded_hits)}")  # => shows expanded query

    assert literal_hits == {0}, (
        "the literal query must find only doc 0, which contains the exact word 'car'"
    )  # => the literal query must find only doc 0, which contains the exact word 'car'
    assert 1 in expanded_hits, (
        "doc 1 (which contains ONLY 'automobile') must be found once synonyms are expanded"
    )  # => doc 1 (which contains ONLY 'automobile') must be found once synonyms are expanded
    assert expanded_hits == {0, 1}, (
        "the expanded query must find exactly docs 0 and 1"
    )  # => the expanded query must find exactly docs 0 and 1
    print(
        f"MATCH: synonym expansion found doc 1's 'automobile' even though the query literally said 'car'"
    )  # => shows MATCH: synonym expansion found doc 1's 'automobile' even though the query literally said 'car'


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
