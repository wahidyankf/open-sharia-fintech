"""Capstone Step 1: pytest suite for the pure core (core.py) -- zero mocking anywhere in this file.

Covers the railway (co-24), the applicative/monoid combine (co-26), the functor .map() calls
(co-25), and two Hypothesis property tests: purity/referential transparency (co-01, co-03) and
the monoid-combine invariant Step 4 asks for -- combining two partial aggregates equals
aggregating the whole file in one pass, checked across many generated inputs, not by hand.
"""

from __future__ import annotations

from hypothesis import given
from hypothesis import strategies as st

from core import (
    EMPTY_TOTALS,
    Err,
    Nothing,
    Ok,
    Row,
    Some,
    Totals,
    aggregate,
    analyze,
    combine_partial_analyses,
    combine_totals,
    format_report,
    keep_positive_amounts,
    map2,
    normalize_categories,
    parse_row,
    parse_rows,
    pipe,
    top_category,
)

# ---------------------------------------------------------------------------
# parse_row: the railway (co-24) -- each malformed shape triggers a DIFFERENT step
# ---------------------------------------------------------------------------


def test_parse_row_accepts_a_well_formed_line() -> None:
    assert parse_row("electronics,199.99") == Ok(
        Row(category="electronics", amount=199.99)
    )


def test_parse_row_rejects_the_wrong_shape() -> None:
    result = parse_row("not-a-valid-row")
    assert isinstance(result, Err)
    assert "malformed row" in result.error


def test_parse_row_rejects_an_empty_category() -> None:
    result = parse_row(",50.00")
    assert isinstance(result, Err)
    assert "category cannot be empty" in result.error


def test_parse_row_rejects_a_non_numeric_amount() -> None:
    result = parse_row("groceries,abc")
    assert isinstance(result, Err)
    assert "not a number" in result.error


def test_parse_row_rejects_a_negative_amount() -> None:
    result = parse_row("books,-5.00")
    assert isinstance(result, Err)
    assert "negative amount" in result.error


def test_parse_row_never_raises_on_malformed_input() -> None:
    # => co-23: failure is a VALUE (Err), never a propagating exception -- this is the whole point
    for bad_line in ("garbage", ",1.00", "x,abc", "x,-1"):
        result = parse_row(
            bad_line
        )  # => must NOT raise -- if it does, this test fails with an error, not an assert
        assert isinstance(result, Err)


# ---------------------------------------------------------------------------
# parse_rows: accumulates EVERY error across the whole file (Step 3's requirement)
# ---------------------------------------------------------------------------


def test_parse_rows_collects_every_malformed_line_not_just_the_first() -> None:
    lines = ["electronics,199.99", "garbage", "groceries,abc", ",50.00", "books,-5.00"]
    result = parse_rows(lines)
    assert isinstance(result, Err)
    assert (
        len(result.error) == 4
    )  # => all FOUR malformed lines are reported, not just the first one


def test_parse_rows_all_valid_returns_ok_of_every_row() -> None:
    lines = ["electronics,199.99", "books,15.25"]
    result = parse_rows(lines)
    assert result == Ok(
        (
            Row(category="electronics", amount=199.99),
            Row(category="books", amount=15.25),
        )
    )


# ---------------------------------------------------------------------------
# aggregate: the pure map/filter/reduce + pipe() composition pipeline (co-11, co-13)
# ---------------------------------------------------------------------------


def test_keep_positive_amounts_drops_zero_amount_rows() -> None:
    rows = (Row("a", 10.0), Row("b", 0.0), Row("c", 5.0))
    assert keep_positive_amounts(rows) == (Row("a", 10.0), Row("c", 5.0))


def test_normalize_categories_lowercases_every_row() -> None:
    rows = (Row("Electronics", 10.0), Row("BOOKS", 5.0))
    assert normalize_categories(rows) == (Row("electronics", 10.0), Row("books", 5.0))


def test_pipe_reads_left_to_right_like_nested_calls() -> None:
    rows = (Row("Electronics", 10.0), Row("Books", 0.0))
    piped = pipe(rows, keep_positive_amounts, normalize_categories)
    nested = normalize_categories(keep_positive_amounts(rows))
    assert piped == nested == (Row("electronics", 10.0),)


def test_aggregate_sums_by_normalized_category_and_drops_zeros() -> None:
    rows = (Row("Electronics", 199.99), Row("electronics", 89.00), Row("Books", 0.0))
    totals = aggregate(rows)
    assert dict(totals.by_category) == {"electronics": 288.99}


def test_aggregate_of_empty_rows_is_the_monoid_identity() -> None:
    assert aggregate(()) == EMPTY_TOTALS


# ---------------------------------------------------------------------------
# combine_totals: the monoid (associativity + identity), map2: the applicative (co-26)
# ---------------------------------------------------------------------------


def test_combine_totals_merges_and_sums_overlapping_categories() -> None:
    a = Totals(by_category={"electronics": 100.0, "books": 5.0})
    b = Totals(by_category={"electronics": 50.0, "groceries": 10.0})
    combined = combine_totals(a, b)
    assert dict(combined.by_category) == {
        "electronics": 150.0,
        "books": 5.0,
        "groceries": 10.0,
    }


def test_combine_totals_identity_law() -> None:
    a = Totals(by_category={"electronics": 100.0})
    assert combine_totals(EMPTY_TOTALS, a) == a  # => left identity
    assert combine_totals(a, EMPTY_TOTALS) == a  # => right identity


def test_combine_totals_never_mutates_either_input() -> None:
    a = Totals(by_category={"electronics": 100.0})
    b = Totals(by_category={"electronics": 50.0})
    combine_totals(a, b)  # => call once, discard the result
    assert dict(a.by_category) == {"electronics": 100.0}  # => a is provably UNCHANGED
    assert dict(b.by_category) == {"electronics": 50.0}  # => b is provably UNCHANGED


def add_ints(
    x: int, y: int
) -> int:  # => a NAMED, fully-typed function -- pins map2's T/U/V at every call
    return (
        x + y
    )  # => a bare lambda here would leave pyright unable to infer T/U from Err-only arguments


def test_map2_combines_two_oks_by_running_fn() -> None:
    result = map2(add_ints, Ok(2), Ok(3))
    assert result == Ok(5)


def test_map2_accumulates_errors_from_both_sides() -> None:
    result = map2(add_ints, Err(("left broke",)), Err(("right broke",)))
    assert result == Err(
        ("left broke", "right broke")
    )  # => BOTH sides reported, co-26 vs co-24's short-circuit


def test_map2_short_circuits_to_the_single_side_that_failed() -> None:
    assert map2(add_ints, Ok(2), Err(("right broke",))) == Err(("right broke",))
    assert map2(add_ints, Err(("left broke",)), Ok(3)) == Err(("left broke",))


# ---------------------------------------------------------------------------
# analyze / combine_partial_analyses: the top-level pure entry points (co-28's pure half)
# ---------------------------------------------------------------------------


VALID_CSV = "category,amount\nElectronics,199.99\nGroceries,45.50\nelectronics,89.00\nBooks,0.00\n"
INVALID_CSV = "category,amount\nElectronics,199.99\ngarbage\nGroceries,abc\n"


def test_analyze_on_valid_csv_returns_ok_totals() -> None:
    result = analyze(VALID_CSV)
    assert isinstance(result, Ok)
    assert dict(result.value.by_category) == {"electronics": 288.99, "groceries": 45.50}


def test_analyze_on_malformed_csv_returns_err_not_an_exception() -> None:
    result = analyze(INVALID_CSV)  # => must NOT raise
    assert isinstance(result, Err)
    assert len(result.error) == 2  # => both malformed rows collected


def test_analyze_called_twice_with_the_same_text_returns_an_equal_result() -> None:
    # => co-03: referential transparency -- the SAME call always substitutes for the SAME value
    assert analyze(VALID_CSV) == analyze(VALID_CSV)


def test_combine_partial_analyses_equals_analyzing_the_whole_file_at_once() -> None:
    # => Step 4's literal acceptance check: split into two files, combine, compare to one pass
    csv_a = "category,amount\nElectronics,199.99\nGroceries,45.50\n"
    csv_b = "category,amount\nelectronics,89.00\nBooks,0.00\n"
    combined = combine_partial_analyses(csv_a, csv_b)
    whole = analyze(
        VALID_CSV
    )  # => VALID_CSV's rows ARE exactly csv_a's rows followed by csv_b's rows
    assert isinstance(combined, Ok) and isinstance(whole, Ok)
    assert dict(combined.value.by_category) == dict(whole.value.by_category)


# ---------------------------------------------------------------------------
# top_category / format_report: Option's functor .map() (co-22, co-25)
# ---------------------------------------------------------------------------


def test_top_category_on_empty_totals_is_nothing() -> None:
    assert top_category(EMPTY_TOTALS) == Nothing()


def test_top_category_on_nonempty_totals_is_some_of_the_largest() -> None:
    totals = Totals(by_category={"books": 5.0, "electronics": 288.99})
    assert top_category(totals) == Some("electronics")


def test_format_report_includes_every_category_and_the_top_line() -> None:
    totals = Totals(by_category={"books": 5.0, "electronics": 288.99})
    report = format_report(totals)
    assert "books: 5.00" in report
    assert "electronics: 288.99" in report
    assert "Top category: electronics" in report


def test_format_report_on_empty_totals_says_so() -> None:
    assert "Top category: (no transactions)" in format_report(EMPTY_TOTALS)


# ---------------------------------------------------------------------------
# Hypothesis property tests (Step 1's "incl. a Hypothesis invariant" requirement)
# ---------------------------------------------------------------------------


category_strategy = st.sampled_from(
    ["electronics", "groceries", "books", "apparel", "toys"]
)
amount_strategy = st.floats(
    min_value=0, max_value=1000, allow_nan=False, allow_infinity=False
).map(
    lambda x: round(
        x, 2
    )  # => rounds to cents -- keeps sums human-checkable, avoids deep float noise
)
row_strategy = st.tuples(category_strategy, amount_strategy)


def rows_to_csv(rows: list[tuple[str, float]]) -> str:
    body = "\n".join(f"{category},{amount}" for category, amount in rows)
    return f"category,amount\n{body}\n" if body else "category,amount\n"


def totals_approx_equal(a: Totals, b: Totals, tolerance: float = 1e-6) -> bool:
    keys = set(a.by_category) | set(
        b.by_category
    )  # => every category mentioned by EITHER side
    return all(
        abs(a.by_category.get(k, 0.0) - b.by_category.get(k, 0.0)) <= tolerance
        for k in keys
    )


@given(rows=st.lists(row_strategy, min_size=0, max_size=20))
def test_property_analyze_is_referentially_transparent(
    rows: list[tuple[str, float]],
) -> None:
    # => co-01/co-03: the SAME csv text, analyzed twice, ALWAYS produces an equal result
    csv_text = rows_to_csv(rows)
    first = analyze(csv_text)
    second = analyze(csv_text)
    assert first == second


@given(
    rows=st.lists(row_strategy, min_size=0, max_size=20),
    split_at=st.integers(min_value=0, max_value=20),
)
def test_property_combining_partial_aggregates_equals_the_whole_in_one_pass(
    rows: list[tuple[str, float]], split_at: int
) -> None:
    # => Step 4's invariant, checked across MANY generated splits, not one hand-picked example
    split_index = min(
        split_at, len(rows)
    )  # => clamps split_at into the valid range for THIS rows list
    left, right = rows[:split_index], rows[split_index:]
    combined = combine_partial_analyses(rows_to_csv(left), rows_to_csv(right))
    whole = analyze(rows_to_csv(rows))
    assert isinstance(combined, Ok)
    assert isinstance(whole, Ok)
    assert totals_approx_equal(
        combined.value, whole.value
    )  # => co-26/monoid: split-then-combine == whole-at-once


@given(
    a=st.dictionaries(category_strategy, amount_strategy),
    b=st.dictionaries(category_strategy, amount_strategy),
)
def test_property_combine_totals_is_associative_with_identity(
    a: dict[str, float], b: dict[str, float]
) -> None:
    totals_a = Totals(by_category=a)
    totals_b = Totals(by_category=b)
    # => the two monoid laws combine_totals must satisfy to genuinely BE a monoid, not just "a merge function"
    assert totals_approx_equal(
        combine_totals(EMPTY_TOTALS, totals_a), totals_a
    )  # => left identity
    assert totals_approx_equal(
        combine_totals(totals_a, EMPTY_TOTALS), totals_a
    )  # => right identity
    assert totals_approx_equal(  # => associativity: grouping never changes the result
        combine_totals(combine_totals(totals_a, totals_b), EMPTY_TOTALS),
        combine_totals(totals_a, combine_totals(totals_b, EMPTY_TOTALS)),
    )


# => Run: pytest -q -- Output: 30 passed
