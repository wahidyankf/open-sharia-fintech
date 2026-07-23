---
title: "Overview"
date: 2026-07-17T00:00:00+07:00
draft: false
weight: 1
---

## Goal

Build a small, real data-processing tool -- a **transaction log analyzer** -- as a **functional
core and imperative shell**: a pure parse-transform-aggregate pipeline built from composition and
`map`/`filter`/`reduce`, `Result`-based error handling instead of exceptions, immutable data
throughout, and a thin I/O shell that reads a CSV file and prints a report. This capstone is a
consolidation, not a new mechanism: every pattern it combines was already taught individually
across the Beginner, Intermediate, and Advanced tiers of this topic (most directly, Example 57's
CSV analyzer, Example 71's error-accumulating validation, and Example 80's capstone-preview log
analyzer).

**The problem**: given a CSV file of `category,amount` transaction rows (one header row, then data
rows), sum the amounts per category, normalize category names so `Electronics` and `electronics`
group together, drop zero-amount rows, and report the totals plus the single highest-grossing
category. A malformed row -- wrong shape, a non-numeric amount, an empty category, or a negative
amount -- must be reported as a collected error, never a crash.

## Concepts exercised

- [x] pure functions + referential transparency (co-01, co-03)
- [x] composition pipeline (co-11, co-13)
- [x] `Result`/`Option` error handling (co-22, co-23, co-24)
- [x] immutability (co-04, co-05)
- [x] functional core / imperative shell split (co-28)
- [x] a functor/applicative/monad pattern used in earnest (co-25, co-26, co-27)

All colocated code lives under `learning/capstone/code/`: the pure functional core in `core.py`,
the imperative shell in `shell.py`, the full `pytest` suites in `test_core.py` and `test_shell.py`,
and two sample CSV files (`sample_transactions.csv`, `bad_transactions.csv`). Every listing below is
the complete file, verbatim -- nothing on this page is truncated or paraphrased.

## Step 1: the pure functional core

_exercises co-01, co-03, co-04, co-05, co-11, co-13, co-22, co-23, co-24, co-25, co-26, co-27_

`core.py` has zero I/O anywhere in it. `Some`/`Nothing` (co-22) and `Ok`/`Err` (co-23) are the same
hand-rolled, generic, immutable containers this topic builds across Examples 48-51, each carrying a
`.map()` -- the functor operation (co-25) that transforms a wrapped value without unwrapping it --
and `Ok`/`Err` additionally carry `.and_then()` -- the monadic chain (co-27) that threads together
Result-returning steps. `parse_row()` chains `split_fields()` -> `validate_category()` ->
`parse_amount_field()` through two `.and_then()` hops: this is the railway (co-24) -- each step only
runs if every prior step already succeeded, and a `ValueError` from `float()` is caught immediately
and turned into an `Err` value, never allowed to propagate (co-23). `parse_rows()` then visits every
line regardless of earlier failures and collects every malformed row into one `Err(tuple[str, ...])`,
so a bad row never stops the rest of the file from being checked. `pipe()` (co-11/co-12) composes
`keep_positive_amounts()` and `normalize_categories()` -- both built from `filter`/`map` (co-13) --
into one left-to-right pipeline that `aggregate()` runs before folding rows into a `Totals` with
`functools.reduce()` (co-13 again). `Totals.by_category` is always a `MappingProxyType` (co-04), and
`add_row()`/`combine_totals()` always build a brand-new `Totals` rather than mutating the one they
were handed (co-05). `combine_totals()` is a genuine **monoid**: associative, with `EMPTY_TOTALS` as
its identity element. `map2()` is the **applicative** combinator (co-26) that combines two
independent `Result`s with a two-argument function, accumulating errors from _both_ sides instead of
short-circuiting at the first one -- the concrete contrast with co-24's railway that co-26's own
definition calls out. `analyze()`, the top-level pure entry point, is `parse_rows(lines).map(aggregate)`
-- co-25's functor `.map()` used in earnest to run `aggregate()` only on the success path, letting a
collected `Err` ride straight through untouched.

**`learning/capstone/code/core.py`** (complete file)

```python
"""Capstone -- Functional Core: Transaction Log Analyzer.

Pure parse -> transform -> aggregate pipeline, zero I/O anywhere in this file. Exercises co-01
(pure functions), co-03 (referential transparency), co-04/co-05 (immutability + structural
sharing via a fresh Totals on every update), co-11/co-13 (a pipe() composition pipeline built
from map/filter/reduce), co-22/co-23 (hand-rolled Option and Result types), co-24 (a railway of
and_then hops inside parse_row), co-25 (Result.map and Option.map used as functors), co-26 (map2,
an applicative combinator for two independent Results), co-27 (and_then/bind chaining
Result-returning steps), and co-28 (this whole file IS the functional core half of the split --
see shell.py for the imperative shell that is the only place with I/O).
"""

from __future__ import annotations  # => enables the quoted 'Option[U]'/'Result[U, F]' forward references below

from collections.abc import Mapping  # => the read-only VIEW type Totals.by_category exposes to callers
from dataclasses import dataclass  # => @dataclass(frozen=True) builds every immutable record/variant here
from functools import reduce  # => reduce folds rows into Totals (co-13) and folds pipe()'s steps (co-11)
from types import MappingProxyType  # => wraps every Totals.by_category dict as read-only (co-04)
from typing import Callable, Generic, TypeVar  # => Generic/TypeVar/Callable type every generic container below

T = TypeVar("T")  # => a generic "value this container wraps" type, reused across Option/Result/pipe
U = TypeVar("U")  # => the type a map/and_then/bind step transforms T into
V = TypeVar("V")  # => the type map2's two-argument function returns
E = TypeVar("E")  # => the type of the error an Err wraps (kept distinct from F below)
F = TypeVar("F")  # => the error type threaded through and_then's step function, not hardcoded to object


# ---------------------------------------------------------------------------
# Option (co-22): "absence" as a value, plus co-25's functor .map()
# ---------------------------------------------------------------------------


@dataclass(frozen=True)  # => marks Some immutable, matching every other record in this file
class Some(Generic[T]):  # => the "present" variant, carrying exactly one value
    value: T  # => the single field this variant carries

    def map(self, fn: Callable[[T], U]) -> "Option[U]":  # => co-25: applies fn INSIDE, without unwrapping
        return Some(fn(self.value))  # => stays wrapped -- Some in, Some out


@dataclass(frozen=True)  # => marks Nothing immutable too
class Nothing:  # => the "absent" variant, carrying nothing at all
    def map(self, fn: Callable[[T], U]) -> "Nothing":  # => NO-OP, generic so a typed fn still type-checks
        return self  # => there is nothing to apply fn to -- Nothing stays Nothing


Option = Some[T] | Nothing  # => PEP 604 union: an Option[T] is either Some[T] or Nothing


# ---------------------------------------------------------------------------
# Result (co-23): success-or-failure as a value, plus co-24/co-25/co-27
# ---------------------------------------------------------------------------


@dataclass(frozen=True)  # => marks Ok immutable, matching the FP style used across this whole topic
class Ok(Generic[T]):  # => the "success" variant, carrying the computed value
    value: T  # => the single field this variant carries

    def map(self, fn: Callable[[T], U]) -> "Ok[U]":  # => co-25: transforms SUCCESS only, error type never widens
        return Ok(fn(self.value))  # => transforms the value, stays wrapped as Ok

    def and_then(  # => co-27: chains into ANOTHER Result-returning step, without double-wrapping
        self, fn: Callable[[T], "Result[U, F]"]  # => F is inferred from fn's own error type
    ) -> "Result[U, F]":  # => closes the multi-line signature above
        return fn(self.value)  # => runs fn on the unwrapped value; fn itself returns a Result


@dataclass(frozen=True)  # => marks Err immutable too
class Err(Generic[E]):  # => the "failure" variant, carrying the ERROR AS A VALUE, never an exception
    error: E  # => the single field this variant carries

    def map(self, fn: Callable[[T], U]) -> "Err[E]":  # => NO-OP: generic so a typed fn still type-checks
        return self  # => the error passes through UNCHANGED -- fn never runs

    def and_then(self, fn: Callable[[T], U]) -> "Err[E]":  # => co-24: the short-circuit half of the railway
        return self  # => once on the failure track, every remaining step is skipped


Result = Ok[T] | Err[E]  # => the ADT itself: a Result is EITHER variant


# ---------------------------------------------------------------------------
# Immutable domain records (co-04)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)  # => one PARSED, immutable transaction row -- never mutated after construction
class Row:  # => the class body begins here
    category: str  # => e.g. "electronics" -- normalized to lowercase by normalize_categories() below
    amount: float  # => a non-negative amount, already validated by the time a Row exists


@dataclass(frozen=True)  # => an immutable per-category rollup
class Totals:  # => the class body begins here
    by_category: Mapping[str, float]  # => always a MappingProxyType -- co-04: read-only from the outside


EMPTY_TOTALS = Totals(by_category=MappingProxyType({}))  # => the monoid IDENTITY element for combine_totals()


# ---------------------------------------------------------------------------
# Composition helper (co-11, co-12): reads left-to-right, execution order
# ---------------------------------------------------------------------------


def pipe(value: T, *fns: Callable[[T], T]) -> T:  # => any number of same-shaped steps, applied IN ORDER
    return reduce(lambda acc, fn: fn(acc), fns, value)  # => co-13: reduce folds each step over the accumulator


# ---------------------------------------------------------------------------
# Row parsing: a railway of Result-returning steps (co-01, co-23, co-24, co-27)
# ---------------------------------------------------------------------------


def split_fields(line: str) -> "Result[tuple[str, str], str]":  # => railway step 1: shape only
    parts = line.split(",", 1)  # => splits "electronics,199.99" into ["electronics", "199.99"]
    if len(parts) != 2:  # => the ONLY thing this step checks -- exactly one comma, two fields
        return Err(f"malformed row (expected 'category,amount'): {line!r}")
    return Ok((parts[0].strip(), parts[1].strip()))  # => success: two trimmed fields, still UNVALIDATED


def validate_category(fields: tuple[str, str]) -> "Result[tuple[str, str], str]":  # => railway step 2
    category, amount_text = fields  # => unpacks the tuple split_fields() already produced
    if category == "":  # => the ONLY thing THIS step checks
        return Err(f"category cannot be empty (amount was {amount_text!r})")
    return Ok(fields)  # => success: fields pass through completely unchanged


def parse_amount_field(fields: tuple[str, str]) -> "Result[Row, str]":  # => railway step 3: builds the Row
    category, amount_text = fields  # => unpacks the tuple the prior two steps already validated
    try:
        amount = float(amount_text)  # => may raise ValueError on "abc" -- CAUGHT below, never escapes
    except ValueError:  # => co-23: the failure becomes a VALUE, not a propagating exception
        return Err(f"invalid amount for {category!r}: {amount_text!r} is not a number")
    if amount < 0:  # => the SECOND check this step makes, only reached once parsing succeeded
        return Err(f"negative amount for {category!r}: {amount_text!r}")
    return Ok(Row(category=category, amount=amount))  # => all three railway steps passed


def parse_row(line: str) -> "Result[Row, str]":  # => co-24: chains all three steps into ONE railway
    return split_fields(line).and_then(validate_category).and_then(parse_amount_field)
    # => co-27: each and_then hop only runs if EVERY prior step already succeeded


def parse_rows(lines: list[str]) -> "Result[tuple[Row, ...], tuple[str, ...]]":  # => across-rows accumulation
    oks: list[Row] = []  # => collects every SUCCESSFULLY parsed row
    errors: list[str] = []  # => collects every FAILURE, across every line, not just the first
    for line in lines:  # => visits EVERY line regardless of earlier failures -- no early return here
        result = parse_row(line)  # => delegates to the pure per-line railway above
        if isinstance(result, Ok):  # => this particular line parsed cleanly
            oks.append(result.value)
        else:  # => this particular line was malformed somewhere along the railway
            errors.append(result.error)  # => a bad line contributes its error, parsing CONTINUES
    if errors:  # => at least one line was malformed
        return Err(tuple(errors))  # => reports EVERY malformed line at once, not just the first
    return Ok(tuple(oks))  # => every line parsed cleanly


# ---------------------------------------------------------------------------
# Pure aggregation pipeline (co-11, co-13)
# ---------------------------------------------------------------------------


def keep_positive_amounts(rows: tuple[Row, ...]) -> tuple[Row, ...]:  # => co-13 filter
    return tuple(filter(lambda row: row.amount > 0, rows))  # => drops zero-amount no-op transactions


def normalize_categories(rows: tuple[Row, ...]) -> tuple[Row, ...]:  # => co-13 map
    return tuple(  # => rebuilds a BRAND NEW tuple -- rows itself is never mutated
        map(lambda row: Row(category=row.category.lower(), amount=row.amount), rows)
    )  # => lowercases category so "Electronics" and "electronics" group together downstream


def add_row(totals: Totals, row: Row) -> Totals:  # => a PURE fold step: returns a NEW Totals, never mutates
    merged = dict(totals.by_category)  # => shallow copy -- co-04/co-05: the OLD totals stays fully intact
    merged[row.category] = merged.get(row.category, 0.0) + row.amount  # => accumulates onto the COPY only
    return Totals(by_category=MappingProxyType(merged))  # => wraps the copy back up as read-only


def aggregate(rows: tuple[Row, ...]) -> Totals:  # => the pure core's aggregation entry point
    cleaned = pipe(rows, keep_positive_amounts, normalize_categories)  # => co-11/co-12: composed pipeline
    return reduce(add_row, cleaned, EMPTY_TOTALS)  # => co-13 reduce: folds cleaned rows into one Totals


# ---------------------------------------------------------------------------
# Monoid combine + applicative map2 (co-26)
# ---------------------------------------------------------------------------


def combine_totals(a: Totals, b: Totals) -> Totals:  # => the MONOID operation: associative, has an identity
    merged = dict(a.by_category)  # => starts from a COPY of a -- a itself is never touched
    for category, amount in b.by_category.items():  # => folds every entry from b onto the copy
        merged[category] = merged.get(category, 0.0) + amount
    return Totals(by_category=MappingProxyType(merged))  # => EMPTY_TOTALS is this operation's identity element


def map2(  # => co-26: the applicative combinator -- combines TWO independently-wrapped Results
    fn: Callable[[T, U], V], a: "Result[T, tuple[str, ...]]", b: "Result[U, tuple[str, ...]]"
) -> "Result[V, tuple[str, ...]]":  # => closes the multi-line signature above
    if isinstance(a, Ok) and isinstance(b, Ok):  # => the ONLY case where fn actually runs
        return Ok(fn(a.value, b.value))  # => unwraps BOTH, applies fn, wraps the combined result back up
    errors: tuple[str, ...] = ()  # => co-26 vs co-24: ACCUMULATES from both sides instead of short-circuiting
    if isinstance(a, Err):  # => a failed -- fold its errors in
        errors += a.error
    if isinstance(b, Err):  # => b failed -- fold its errors in TOO, even if a already failed
        errors += b.error
    return Err(errors)  # => reports every failing side at once, not just the first one found


# ---------------------------------------------------------------------------
# Top-level pure entry points
# ---------------------------------------------------------------------------


def analyze(csv_text: str) -> "Result[Totals, tuple[str, ...]]":  # => PURE CORE: text in, Result out, no I/O
    lines = csv_text.strip().splitlines()[1:]  # => drops the header row, e.g. "category,amount"
    return parse_rows(lines).map(aggregate)  # => co-25 functor: transforms success, error rides through untouched


def combine_partial_analyses(  # => opens the multi-line signature of the monoid-combine entry point
    csv_text_a: str, csv_text_b: str  # => two independently self-headered "files"
) -> "Result[Totals, tuple[str, ...]]":  # => closes the multi-line signature above
    return map2(combine_totals, analyze(csv_text_a), analyze(csv_text_b))  # => co-26 applicative + monoid combine


def top_category(totals: Totals) -> "Option[str]":  # => co-22: absence is a VALUE, not a None landmine
    if not totals.by_category:  # => nothing was ever aggregated
        return Nothing()
    best = max(totals.by_category.items(), key=lambda pair: pair[1])  # => (category, amount) with the max total
    return Some(best[0])


def format_report(totals: Totals) -> str:  # => still PURE: data -> text, zero I/O
    lines = [f"{category}: {amount:.2f}" for category, amount in sorted(totals.by_category.items())]
    headline = top_category(totals).map(  # => co-25 functor: Option.map builds the headline INSIDE the wrapper
        lambda category: f"Top category: {category}"
    )
    if isinstance(headline, Some):  # => a category actually exists
        lines.append(headline.value)
    else:  # => totals.by_category was empty -- top_category() returned Nothing
        lines.append("Top category: (no transactions)")
    return "\n".join(lines)  # => a plain string -- the shell decides how to display it
```

**`learning/capstone/code/test_core.py`** (complete file)

```python
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
    assert parse_row("electronics,199.99") == Ok(Row(category="electronics", amount=199.99))


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
        result = parse_row(bad_line)  # => must NOT raise -- if it does, this test fails with an error, not an assert
        assert isinstance(result, Err)


# ---------------------------------------------------------------------------
# parse_rows: accumulates EVERY error across the whole file (Step 3's requirement)
# ---------------------------------------------------------------------------


def test_parse_rows_collects_every_malformed_line_not_just_the_first() -> None:
    lines = ["electronics,199.99", "garbage", "groceries,abc", ",50.00", "books,-5.00"]
    result = parse_rows(lines)
    assert isinstance(result, Err)
    assert len(result.error) == 4  # => all FOUR malformed lines are reported, not just the first one


def test_parse_rows_all_valid_returns_ok_of_every_row() -> None:
    lines = ["electronics,199.99", "books,15.25"]
    result = parse_rows(lines)
    assert result == Ok((Row(category="electronics", amount=199.99), Row(category="books", amount=15.25)))


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
    assert dict(combined.by_category) == {"electronics": 150.0, "books": 5.0, "groceries": 10.0}


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


def add_ints(x: int, y: int) -> int:  # => a NAMED, fully-typed function -- pins map2's T/U/V at every call
    return x + y  # => a bare lambda here would leave pyright unable to infer T/U from Err-only arguments


def test_map2_combines_two_oks_by_running_fn() -> None:
    result = map2(add_ints, Ok(2), Ok(3))
    assert result == Ok(5)


def test_map2_accumulates_errors_from_both_sides() -> None:
    result = map2(add_ints, Err(("left broke",)), Err(("right broke",)))
    assert result == Err(("left broke", "right broke"))  # => BOTH sides reported, co-26 vs co-24's short-circuit


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
    whole = analyze(VALID_CSV)  # => VALID_CSV's rows ARE exactly csv_a's rows followed by csv_b's rows
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


category_strategy = st.sampled_from(["electronics", "groceries", "books", "apparel", "toys"])
amount_strategy = st.floats(min_value=0, max_value=1000, allow_nan=False, allow_infinity=False).map(
    lambda x: round(x, 2)  # => rounds to cents -- keeps sums human-checkable, avoids deep float noise
)
row_strategy = st.tuples(category_strategy, amount_strategy)


def rows_to_csv(rows: list[tuple[str, float]]) -> str:
    body = "\n".join(f"{category},{amount}" for category, amount in rows)
    return f"category,amount\n{body}\n" if body else "category,amount\n"


def totals_approx_equal(a: Totals, b: Totals, tolerance: float = 1e-6) -> bool:
    keys = set(a.by_category) | set(b.by_category)  # => every category mentioned by EITHER side
    return all(abs(a.by_category.get(k, 0.0) - b.by_category.get(k, 0.0)) <= tolerance for k in keys)


@given(rows=st.lists(row_strategy, min_size=0, max_size=20))
def test_property_analyze_is_referentially_transparent(rows: list[tuple[str, float]]) -> None:
    # => co-01/co-03: the SAME csv text, analyzed twice, ALWAYS produces an equal result
    csv_text = rows_to_csv(rows)
    first = analyze(csv_text)
    second = analyze(csv_text)
    assert first == second


@given(rows=st.lists(row_strategy, min_size=0, max_size=20), split_at=st.integers(min_value=0, max_value=20))
def test_property_combining_partial_aggregates_equals_the_whole_in_one_pass(
    rows: list[tuple[str, float]], split_at: int
) -> None:
    # => Step 4's invariant, checked across MANY generated splits, not one hand-picked example
    split_index = min(split_at, len(rows))  # => clamps split_at into the valid range for THIS rows list
    left, right = rows[:split_index], rows[split_index:]
    combined = combine_partial_analyses(rows_to_csv(left), rows_to_csv(right))
    whole = analyze(rows_to_csv(rows))
    assert isinstance(combined, Ok)
    assert isinstance(whole, Ok)
    assert totals_approx_equal(combined.value, whole.value)  # => co-26/monoid: split-then-combine == whole-at-once


@given(a=st.dictionaries(category_strategy, amount_strategy), b=st.dictionaries(category_strategy, amount_strategy))
def test_property_combine_totals_is_associative_with_identity(a: dict[str, float], b: dict[str, float]) -> None:
    totals_a = Totals(by_category=a)
    totals_b = Totals(by_category=b)
    # => the two monoid laws combine_totals must satisfy to genuinely BE a monoid, not just "a merge function"
    assert totals_approx_equal(combine_totals(EMPTY_TOTALS, totals_a), totals_a)  # => left identity
    assert totals_approx_equal(combine_totals(totals_a, EMPTY_TOTALS), totals_a)  # => right identity
    assert totals_approx_equal(  # => associativity: grouping never changes the result
        combine_totals(combine_totals(totals_a, totals_b), EMPTY_TOTALS),
        combine_totals(totals_a, combine_totals(totals_b, EMPTY_TOTALS)),
    )


# => Run: pytest -q -- Output: 30 passed
```

**Verify**

```shell
pip install -r requirements.txt
python3 -m pytest test_core.py -q
```

**Output**

```text
30 passed
```

## Step 2: the imperative shell

_exercises co-28_

`shell.py`'s `main()` is the only function in this entire capstone that touches the filesystem or
prints anything -- `Path.read_text()` reads the CSV, `analyze()` (all logic) runs entirely inside
`core.py`, and `print()` writes the report or the collected errors. No parsing, validation, or
aggregation logic lives in this file at all; `main()` is a thin dispatcher between three pure calls
(`analyze`, the `isinstance` check, `format_report`) and the two I/O boundaries around them.

**`learning/capstone/code/shell.py`** (complete file)

```python
"""Capstone -- Imperative Shell: reads a transaction CSV file and prints the report.

Exercises co-28's OTHER half: main() is the ONLY function in this whole capstone that performs
I/O (reading a file, writing to stdout/stderr). Every actual computation -- parsing, validating,
aggregating, formatting -- is delegated straight to core.py's pure functions; this file holds no
transformation logic of its own at all.
"""

from __future__ import annotations

import sys  # => sys.argv (read) and sys.exit (write the process exit code) -- both I/O boundaries
from pathlib import Path  # => Path.read_text() is this shell's ONE file-reading I/O boundary

from core import Err, analyze, format_report  # => everything computational comes from the pure core


def main(argv: list[str]) -> int:  # => the IMPERATIVE SHELL entry point -- the ONLY place with I/O
    if len(argv) != 1:  # => a tiny bit of shell-level argument handling, still not "business logic"
        print("usage: shell.py <transactions.csv>", file=sys.stderr)  # => I/O boundary: stderr
        return 2  # => a non-zero exit code signals misuse to the calling shell/CI
    path = Path(argv[0])  # => resolves the CLI argument into a filesystem path -- no read yet
    csv_text = path.read_text()  # => I/O boundary: the ONE file read in this entire capstone
    result = analyze(csv_text)  # => delegates EVERYTHING else to the pure core -- zero logic here
    if isinstance(result, Err):  # => malformed input: report every collected error, do NOT crash
        print(f"{len(result.error)} error(s) found:")  # => I/O boundary: stdout
        for message in result.error:  # => walks EVERY accumulated error, not just the first
            print(f"  {message}")  # => one printed line per malformed input row
        return 1  # => a non-zero exit code signals "input had errors" to the calling shell/CI
    print(format_report(result.value))  # => I/O boundary: prints the pure core's own report string
    return 0  # => success


if __name__ == "__main__":  # => only runs when invoked directly, e.g. `python3 shell.py sample.csv`
    sys.exit(main(sys.argv[1:]))  # => argv[0] is the script name itself -- argv[1:] is the real arguments
```

**`learning/capstone/code/sample_transactions.csv`** (complete file)

```text
category,amount
Electronics,199.99
Groceries,45.50
electronics,89.00
Books,15.25
Groceries,12.75
Apparel,60.00
Books,0.00
```

**Run**

```shell
python3 shell.py sample_transactions.csv
```

**Output**

```text
apparel: 60.00
books: 15.25
electronics: 288.99
groceries: 58.25
Top category: electronics
```

`Electronics,199.99` and `electronics,89.00` merged into one `288.99` total under `normalize_categories()`;
`Books,0.00` never reaches the totals at all because `keep_positive_amounts()` dropped it.

**`learning/capstone/code/test_shell.py`** (complete file)

```python
"""Capstone Step 2: verifies shell.py end to end, as a REAL subprocess CLI invocation.

Runs `python3 shell.py <file>` exactly the way a user would from a terminal, and checks the
captured stdout/exit code -- the strongest form of "runs end to end from the CLI" this capstone
can demonstrate, stronger than calling main() in-process.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

CODE_DIR = Path(__file__).parent
SHELL_PATH = CODE_DIR / "shell.py"
SAMPLE_CSV = CODE_DIR / "sample_transactions.csv"
BAD_CSV = CODE_DIR / "bad_transactions.csv"


def run_shell(*args: str) -> subprocess.CompletedProcess[str]:  # => the ONE helper every test below reuses
    return subprocess.run(  # => a REAL child process, exactly like a user typing this at a terminal
        [sys.executable, str(SHELL_PATH), *args],
        capture_output=True,
        text=True,
        check=False,  # => this suite inspects returncode itself -- a non-zero exit is a valid case, not a crash
    )


def test_shell_on_valid_csv_prints_the_report_and_exits_zero() -> None:
    completed = run_shell(str(SAMPLE_CSV))
    assert completed.returncode == 0
    assert "electronics: 288.99" in completed.stdout
    assert "groceries: 58.25" in completed.stdout
    assert "books: 15.25" in completed.stdout
    assert "apparel: 60.00" in completed.stdout
    assert "Top category: electronics" in completed.stdout


def test_shell_on_malformed_csv_reports_errors_and_exits_nonzero_without_crashing() -> None:
    completed = run_shell(str(BAD_CSV))
    assert completed.returncode == 1  # => a controlled non-zero exit -- NOT a Python traceback
    assert "4 error(s) found" in completed.stdout
    assert "Traceback" not in completed.stderr  # => co-23: proves the shell never let an exception escape


def test_shell_with_no_arguments_prints_usage_and_exits_two() -> None:
    completed = run_shell()
    assert completed.returncode == 2
    assert "usage: shell.py" in completed.stderr


# => Run: pytest -q -- Output: 3 passed
```

**Verify**

```shell
python3 -m pytest test_shell.py -q
```

**Output**

```text
3 passed
```

## Step 3: Result replaces exceptions -- grounded against `bad_transactions.csv`

_exercises co-23, co-24_

The core built in Step 1 never used exceptions for malformed input in the first place --
`parse_amount_field()` catches the one place a real exception could occur (`float()` on a
non-numeric string) and turns it straight into an `Err` value. Running `parse_row()` directly
against every kind of malformed line confirms the same thing this topic's tests already check
(`test_parse_row_never_raises_on_malformed_input`): every failure comes back as a value, not a
traceback.

**Run**

```shell
python3 -c "
from core import parse_row
for bad_line in ['garbage', ',1.00', 'x,abc', 'x,-1']:
    print(f'{bad_line!r:>12} -> {parse_row(bad_line)}')
"
```

**Output**

```text
   'garbage' -> Err(error="malformed row (expected 'category,amount'): 'garbage'")
     ',1.00' -> Err(error="category cannot be empty (amount was '1.00')")
     'x,abc' -> Err(error="invalid amount for 'x': 'abc' is not a number")
      'x,-1' -> Err(error="negative amount for 'x': '-1'")
```

**`learning/capstone/code/bad_transactions.csv`** (complete file)

```text
category,amount
Electronics,199.99
BadRow
Groceries,abc
,50.00
Books,-5.00
```

**Run**

```shell
python3 shell.py bad_transactions.csv
```

**Output**

```text
4 error(s) found:
  malformed row (expected 'category,amount'): 'BadRow'
  invalid amount for 'Groceries': 'abc' is not a number
  category cannot be empty (amount was '50.00')
  negative amount for 'Books': '-5.00'
```

The one genuinely valid row (`Electronics,199.99`) never appears in this output at all -- once
`parse_rows()` finds any error, `analyze()`'s `Err` path takes over and no partial report is
printed, exactly the acceptance criterion Step 3 asks for: malformed rows yield a _collected error
result_, never a crash, and never a silently-partial report either.
`test_analyze_on_malformed_csv_returns_err_not_an_exception`,
`test_parse_rows_collects_every_malformed_line_not_just_the_first`, and
`test_shell_on_malformed_csv_reports_errors_and_exits_nonzero_without_crashing` all check this same
guarantee from three different layers -- the pure row parser, the pure file-level aggregator, and
the real subprocess CLI.

## Step 4: a functor/applicative/monoid pattern used in earnest

_exercises co-25, co-26, co-27_

Splitting `sample_transactions.csv`'s rows into two independent CSV "files", analyzing each half
separately, and combining the two partial `Totals` with `map2(combine_totals, ...)` produces the
exact same result as analyzing the whole file in one pass -- the concrete demonstration this
capstone's own Step 4 asks for.

**Run**

```shell
python3 -c "
from core import analyze, combine_partial_analyses, Ok

csv_a = 'category,amount\nElectronics,199.99\nGroceries,45.50\n'
csv_b = 'category,amount\nelectronics,89.00\nBooks,0.00\n'
whole = 'category,amount\nElectronics,199.99\nGroceries,45.50\nelectronics,89.00\nBooks,0.00\n'

combined = combine_partial_analyses(csv_a, csv_b)
one_pass = analyze(whole)
assert isinstance(combined, Ok) and isinstance(one_pass, Ok)
print('combined:', dict(combined.value.by_category))
print('one_pass:', dict(one_pass.value.by_category))
print('equal:', dict(combined.value.by_category) == dict(one_pass.value.by_category))
"
```

**Output**

```text
combined: {'electronics': 288.99, 'groceries': 45.5}
one_pass: {'electronics': 288.99, 'groceries': 45.5}
equal: True
```

Three concepts are in play together here, not just one. `analyze()` uses the **functor** pattern
(co-25) -- `parse_rows(lines).map(aggregate)` transforms the success value without ever unwrapping
the `Result` by hand. `map2()` is the **applicative** pattern (co-26) -- it combines _two_
independently-produced `Result`s (`analyze(csv_a)` and `analyze(csv_b)`) with the two-argument
`combine_totals()`, and if malformed rows exist on both sides, `map2()` accumulates _both_ sets of
errors instead of reporting only one, which `test_map2_accumulates_errors_from_both_sides` checks
directly. `parse_row()`'s own `.and_then()` chain is the **monad** pattern (co-27) already exercised
throughout Step 1. `combine_totals()` is additionally a genuine monoid: `test_combine_totals_identity_law`
checks `combine_totals(EMPTY_TOTALS, a) == a` in both directions, and the Hypothesis property
`test_property_combine_totals_is_associative_with_identity` checks associativity and identity across
many generated `Totals` pairs, not one hand-picked example. Finally,
`test_property_combining_partial_aggregates_equals_the_whole_in_one_pass` generalizes the exact
demonstration above into a property test: for many randomly generated row lists and split points,
splitting, analyzing each half, and combining always equals analyzing the whole file in one pass.

## Done bar

**Runnable end to end**: `python3 shell.py sample_transactions.csv` prints the five-line report
above and exits `0`; `python3 shell.py bad_transactions.csv` prints the four collected errors and
exits `1`; `python3 shell.py` with no arguments prints a usage line to `stderr` and exits `2`.

**Full suite**: `pip install -r requirements.txt && python3 -m pytest -q` from
`learning/capstone/code/` runs `test_core.py` (30 tests, including three Hypothesis property tests)
and `test_shell.py` (3 subprocess-driven CLI tests):

```text
33 passed
```

**Type safety**: `pyright` in `--strict` mode (`pyrightconfig.json` sets
`"typeCheckingMode": "strict"`) against every file in `learning/capstone/code/`:

```text
0 errors, 0 warnings, 0 informations
```

**Acceptance criteria, verified against specific code and tests**: the core (`core.py`) is pure and
tested without mocks (`test_core.py` imports nothing but `core` and `hypothesis`); errors are values,
never exceptions (`parse_amount_field()`'s `try`/`except` converts the one possible `ValueError` into
an `Err`, and `test_parse_row_never_raises_on_malformed_input` / `test_analyze_on_malformed_csv_returns_err_not_an_exception`
/ `test_shell_on_malformed_csv_reports_errors_and_exits_nonzero_without_crashing` all check it); the
shell (`shell.py`) is the only place with I/O (`Path.read_text()` and every `print()` call live
exclusively inside `main()`); and the tool runs end to end, both directly (the **Run** blocks above)
and under `pytest` (`test_shell.py`'s subprocess-driven suite).

---

← Previous: [Advanced Examples](../advanced.md) &middot; Next: [Drilling](../../drilling/overview.md) →
