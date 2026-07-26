# pyright: strict
"""Example 52: Query DSL Execute (co-26)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from dataclasses import dataclass  # => from dataclasses: dataclass


@dataclass(
    frozen=True
)  # => part of this step's computation, continued from the line above
class BoolQuery:  # => part of this step's computation, continued from the line above
    must: tuple[str, ...] = ()  # => must = ()
    should: tuple[str, ...] = ()  # => should = ()
    must_not: tuple[str, ...] = ()  # => must not = ()


def execute_query(
    index: dict[str, set[int]], query: BoolQuery
) -> set[int]:  # => execute a parsed BoolQuery tree against a term -> doc-id-set index
    """Execute a parsed BoolQuery tree against a term -> doc-id-set index."""
    all_docs: set[int] = (
        set[int]().union(*index.values()) if index else set[int]()
    )  # => co-03: the universe, for must_not/should defaults
    result: set[int] = set(
        all_docs
    )  # => starts as "everything," narrowed by each clause below
    for (
        term
    ) in query.must:  # => co-26: AND -- every must term narrows the result further
        result &= index.get(
            term, set()
        )  # => part of this step's computation, continued from the line above
    if query.should:  # => co-26: OR, but only if the should list is non-empty
        should_hits: set[int] = set()  # => should hits = set()
        for term in query.should:  # => iterates one item at a time
            should_hits |= index.get(
                term, set()
            )  # => part of this step's computation, continued from the line above
        result &= should_hits  # => part of this step's computation, continued from the line above
    for term in (
        query.must_not
    ):  # => co-26: AND-NOT -- removes anything matching a must_not term
        result -= index.get(
            term, set()
        )  # => part of this step's computation, continued from the line above
    return result  # => returns result


def main() -> None:  # => defines main
    index: dict[str, set[int]] = {  # => a small inverted index, term -> doc-ids
        "search": {0, 1, 2, 3},  # => entry for 'search'
        "engine": {0, 1, 4},  # => entry for 'engine'
        "fast": {1, 3},  # => entry for 'fast'
        "deprecated": {3},  # => entry for 'deprecated'
    }  # => opens/closes this multi-line literal
    query = BoolQuery(
        must=("search", "engine"), should=("fast",), must_not=("deprecated",)
    )  # => co-26: must both terms, prefer fast, exclude deprecated
    result: set[int] = execute_query(index, query)  # => co-26: the tree-based execution
    print(
        f"query: must={query.must} should={query.should} must_not={query.must_not}"
    )  # => shows query: must=
    print(f"result: {sorted(result)}")  # => shows result

    # An equivalent HAND-WRITTEN boolean merge, computed a completely different way.
    hand_must: set[int] = index["search"] & index["engine"]  # => {0, 1}
    hand_with_should: set[int] = hand_must & index["fast"]  # => {0, 1} & {1, 3} = {1}
    hand_result: set[int] = hand_with_should - index["deprecated"]  # => {1} - {3} = {1}
    assert result == hand_result, (
        "execute_query's result must equal the hand-written boolean merge"
    )  # => execute_query's result must equal the hand-written boolean merge
    print(
        f"MATCH: execute_query's result {sorted(result)} equals the hand-written merge {sorted(hand_result)}"
    )  # => shows MATCH: execute_query's result


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
