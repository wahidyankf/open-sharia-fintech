"""Example 66: pytest verification for Paradigm Decision Record."""

from example import DECISION_TABLE


def test_every_row_cites_a_concrete_selection_criterion() -> None:
    for row in DECISION_TABLE:  # => every row must justify itself, not just assert a paradigm name
        assert row.selection_criterion != ""  # => a non-empty criterion is present
        assert "see ex-" in row.selection_criterion  # => and it points back at concrete worked examples


def test_table_has_at_least_one_row_per_major_paradigm_family() -> None:
    paradigms = {row.recommended_paradigm for row in DECISION_TABLE}
    assert any("constraint" in p or "logic" in p for p in paradigms)  # => search-flavored problems covered
    assert any("reactive" in p for p in paradigms)  # => sync-flavored problems covered
    assert any("functional" in p for p in paradigms)  # => transformation-flavored problems covered


# => Run: pytest -- Output: 2 passed
