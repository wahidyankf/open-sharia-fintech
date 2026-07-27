# pyright: strict
"""Example 51: Query DSL Parse (co-26)."""

from __future__ import (
    annotations,
)  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from dataclasses import dataclass  # => from dataclasses: dataclass


@dataclass(
    frozen=True
)  # => part of this step's computation, continued from the line above
class BoolQuery:  # => part of this step's computation, continued from the line above
    """A parsed boolean query tree: AND (must), OR (should), AND-NOT (must_not)."""

    must: tuple[str, ...] = ()  # => co-26: every term here MUST be present
    should: tuple[
        str, ...
    ] = ()  # => co-26: at least ONE of these must be present, if the list is non-empty
    must_not: tuple[str, ...] = ()  # => co-26: NONE of these may be present


def parse_query_dsl(
    raw: dict[str, list[str]],
) -> BoolQuery:  # => parse a raw {"must": [...], "should": [...], "must_not": [...]} dict into a BoolQuery tree
    """Parse a raw {"must": [...], "should": [...], "must_not": [...]} dict into a BoolQuery tree."""
    return BoolQuery(  # => co-26: builds the typed tree from the untyped raw DSL
        must=tuple(raw.get("must", [])),  # => must = tuple(raw.get("must", [])),
        should=tuple(
            raw.get("should", [])
        ),  # => should = tuple(raw.get("should", [])),
        must_not=tuple(
            raw.get("must_not", [])
        ),  # => must not = tuple(raw.get("must_not", [])),
    )  # => opens/closes this multi-line literal


def main() -> None:  # => defines main
    raw_dsl: dict[
        str, list[str]
    ] = {  # => a query DSL as an untyped dict, the way a JSON request body would arrive
        "must": ["search", "engine"],  # => entry for 'must'
        "should": ["fast", "reliable"],  # => entry for 'should'
        "must_not": ["deprecated"],  # => entry for 'must_not'
    }  # => opens/closes this multi-line literal
    query: BoolQuery = parse_query_dsl(
        raw_dsl
    )  # => co-26: the parsed, typed query tree
    print(
        f"parsed query: must={query.must} should={query.should} must_not={query.must_not}"
    )  # => shows parsed query: must=

    assert query.must == ("search", "engine"), (
        "must must contain exactly the DSL's 'must' terms, in order"
    )  # => must must contain exactly the DSL's 'must' terms, in order
    assert query.should == ("fast", "reliable"), (
        "should must contain exactly the DSL's 'should' terms, in order"
    )  # => should must contain exactly the DSL's 'should' terms, in order
    assert query.must_not == ("deprecated",), (
        "must_not must contain exactly the DSL's 'must_not' terms"
    )  # => must_not must contain exactly the DSL's 'must_not' terms
    print(
        "MATCH: the parsed tree's must/should/must_not fields each hold exactly the DSL's own terms"
    )  # => shows MATCH: the parsed tree's must/should/must_not fields each hold exactly the DSL's own terms


if (
    __name__ == "__main__"
):  # => entry point -- runs only when this file executes directly, not on import
    main()  # => runs the example end to end
