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

from __future__ import (
    annotations,
)  # => enables the quoted 'Option[U]'/'Result[U, F]' forward references below

from collections.abc import (
    Mapping,
)  # => the read-only VIEW type Totals.by_category exposes to callers
from dataclasses import (
    dataclass,
)  # => @dataclass(frozen=True) builds every immutable record/variant here
from functools import (
    reduce,
)  # => reduce folds rows into Totals (co-13) and folds pipe()'s steps (co-11)
from types import (
    MappingProxyType,
)  # => wraps every Totals.by_category dict as read-only (co-04)
from typing import (
    Callable,
    Generic,
    TypeVar,
)  # => Generic/TypeVar/Callable type every generic container below

T = TypeVar(
    "T"
)  # => a generic "value this container wraps" type, reused across Option/Result/pipe
U = TypeVar("U")  # => the type a map/and_then/bind step transforms T into
V = TypeVar("V")  # => the type map2's two-argument function returns
E = TypeVar("E")  # => the type of the error an Err wraps (kept distinct from F below)
F = TypeVar(
    "F"
)  # => the error type threaded through and_then's step function, not hardcoded to object


# ---------------------------------------------------------------------------
# Option (co-22): "absence" as a value, plus co-25's functor .map()
# ---------------------------------------------------------------------------


@dataclass(
    frozen=True
)  # => marks Some immutable, matching every other record in this file
class Some(Generic[T]):  # => the "present" variant, carrying exactly one value
    value: T  # => the single field this variant carries

    def map(
        self, fn: Callable[[T], U]
    ) -> "Option[U]":  # => co-25: applies fn INSIDE, without unwrapping
        return Some(fn(self.value))  # => stays wrapped -- Some in, Some out


@dataclass(frozen=True)  # => marks Nothing immutable too
class Nothing:  # => the "absent" variant, carrying nothing at all
    def map(
        self, fn: Callable[[T], U]
    ) -> "Nothing":  # => NO-OP, generic so a typed fn still type-checks
        return self  # => there is nothing to apply fn to -- Nothing stays Nothing


Option = (
    Some[T] | Nothing
)  # => PEP 604 union: an Option[T] is either Some[T] or Nothing


# ---------------------------------------------------------------------------
# Result (co-23): success-or-failure as a value, plus co-24/co-25/co-27
# ---------------------------------------------------------------------------


@dataclass(
    frozen=True
)  # => marks Ok immutable, matching the FP style used across this whole topic
class Ok(Generic[T]):  # => the "success" variant, carrying the computed value
    value: T  # => the single field this variant carries

    def map(
        self, fn: Callable[[T], U]
    ) -> "Ok[U]":  # => co-25: transforms SUCCESS only, error type never widens
        return Ok(fn(self.value))  # => transforms the value, stays wrapped as Ok

    def and_then(  # => co-27: chains into ANOTHER Result-returning step, without double-wrapping
        self,
        fn: Callable[[T], "Result[U, F]"],  # => F is inferred from fn's own error type
    ) -> "Result[U, F]":  # => closes the multi-line signature above
        return fn(
            self.value
        )  # => runs fn on the unwrapped value; fn itself returns a Result


@dataclass(frozen=True)  # => marks Err immutable too
class Err(
    Generic[E]
):  # => the "failure" variant, carrying the ERROR AS A VALUE, never an exception
    error: E  # => the single field this variant carries

    def map(
        self, fn: Callable[[T], U]
    ) -> "Err[E]":  # => NO-OP: generic so a typed fn still type-checks
        return self  # => the error passes through UNCHANGED -- fn never runs

    def and_then(
        self, fn: Callable[[T], U]
    ) -> "Err[E]":  # => co-24: the short-circuit half of the railway
        return self  # => once on the failure track, every remaining step is skipped


Result = Ok[T] | Err[E]  # => the ADT itself: a Result is EITHER variant


# ---------------------------------------------------------------------------
# Immutable domain records (co-04)
# ---------------------------------------------------------------------------


@dataclass(
    frozen=True
)  # => one PARSED, immutable transaction row -- never mutated after construction
class Row:  # => the class body begins here
    category: str  # => e.g. "electronics" -- normalized to lowercase by normalize_categories() below
    amount: (
        float  # => a non-negative amount, already validated by the time a Row exists
    )


@dataclass(frozen=True)  # => an immutable per-category rollup
class Totals:  # => the class body begins here
    by_category: Mapping[
        str, float
    ]  # => always a MappingProxyType -- co-04: read-only from the outside


EMPTY_TOTALS = Totals(
    by_category=MappingProxyType({})
)  # => the monoid IDENTITY element for combine_totals()


# ---------------------------------------------------------------------------
# Composition helper (co-11, co-12): reads left-to-right, execution order
# ---------------------------------------------------------------------------


def pipe(
    value: T, *fns: Callable[[T], T]
) -> T:  # => any number of same-shaped steps, applied IN ORDER
    return reduce(
        lambda acc, fn: fn(acc), fns, value
    )  # => co-13: reduce folds each step over the accumulator


# ---------------------------------------------------------------------------
# Row parsing: a railway of Result-returning steps (co-01, co-23, co-24, co-27)
# ---------------------------------------------------------------------------


def split_fields(
    line: str,
) -> "Result[tuple[str, str], str]":  # => railway step 1: shape only
    parts = line.split(
        ",", 1
    )  # => splits "electronics,199.99" into ["electronics", "199.99"]
    if (
        len(parts) != 2
    ):  # => the ONLY thing this step checks -- exactly one comma, two fields
        return Err(f"malformed row (expected 'category,amount'): {line!r}")
    return Ok(
        (parts[0].strip(), parts[1].strip())
    )  # => success: two trimmed fields, still UNVALIDATED


def validate_category(
    fields: tuple[str, str],
) -> "Result[tuple[str, str], str]":  # => railway step 2
    category, amount_text = (
        fields  # => unpacks the tuple split_fields() already produced
    )
    if category == "":  # => the ONLY thing THIS step checks
        return Err(f"category cannot be empty (amount was {amount_text!r})")
    return Ok(fields)  # => success: fields pass through completely unchanged


def parse_amount_field(
    fields: tuple[str, str],
) -> "Result[Row, str]":  # => railway step 3: builds the Row
    category, amount_text = (
        fields  # => unpacks the tuple the prior two steps already validated
    )
    try:
        amount = float(
            amount_text
        )  # => may raise ValueError on "abc" -- CAUGHT below, never escapes
    except (
        ValueError
    ):  # => co-23: the failure becomes a VALUE, not a propagating exception
        return Err(f"invalid amount for {category!r}: {amount_text!r} is not a number")
    if (
        amount < 0
    ):  # => the SECOND check this step makes, only reached once parsing succeeded
        return Err(f"negative amount for {category!r}: {amount_text!r}")
    return Ok(
        Row(category=category, amount=amount)
    )  # => all three railway steps passed


def parse_row(
    line: str,
) -> "Result[Row, str]":  # => co-24: chains all three steps into ONE railway
    return split_fields(line).and_then(validate_category).and_then(parse_amount_field)
    # => co-27: each and_then hop only runs if EVERY prior step already succeeded


def parse_rows(
    lines: list[str],
) -> "Result[tuple[Row, ...], tuple[str, ...]]":  # => across-rows accumulation
    oks: list[Row] = []  # => collects every SUCCESSFULLY parsed row
    errors: list[
        str
    ] = []  # => collects every FAILURE, across every line, not just the first
    for line in (
        lines
    ):  # => visits EVERY line regardless of earlier failures -- no early return here
        result = parse_row(line)  # => delegates to the pure per-line railway above
        if isinstance(result, Ok):  # => this particular line parsed cleanly
            oks.append(result.value)
        else:  # => this particular line was malformed somewhere along the railway
            errors.append(
                result.error
            )  # => a bad line contributes its error, parsing CONTINUES
    if errors:  # => at least one line was malformed
        return Err(
            tuple(errors)
        )  # => reports EVERY malformed line at once, not just the first
    return Ok(tuple(oks))  # => every line parsed cleanly


# ---------------------------------------------------------------------------
# Pure aggregation pipeline (co-11, co-13)
# ---------------------------------------------------------------------------


def keep_positive_amounts(rows: tuple[Row, ...]) -> tuple[Row, ...]:  # => co-13 filter
    return tuple(
        filter(lambda row: row.amount > 0, rows)
    )  # => drops zero-amount no-op transactions


def normalize_categories(rows: tuple[Row, ...]) -> tuple[Row, ...]:  # => co-13 map
    return tuple(  # => rebuilds a BRAND NEW tuple -- rows itself is never mutated
        map(lambda row: Row(category=row.category.lower(), amount=row.amount), rows)
    )  # => lowercases category so "Electronics" and "electronics" group together downstream


def add_row(
    totals: Totals, row: Row
) -> Totals:  # => a PURE fold step: returns a NEW Totals, never mutates
    merged = dict(
        totals.by_category
    )  # => shallow copy -- co-04/co-05: the OLD totals stays fully intact
    merged[row.category] = (
        merged.get(row.category, 0.0) + row.amount
    )  # => accumulates onto the COPY only
    return Totals(
        by_category=MappingProxyType(merged)
    )  # => wraps the copy back up as read-only


def aggregate(
    rows: tuple[Row, ...],
) -> Totals:  # => the pure core's aggregation entry point
    cleaned = pipe(
        rows, keep_positive_amounts, normalize_categories
    )  # => co-11/co-12: composed pipeline
    return reduce(
        add_row, cleaned, EMPTY_TOTALS
    )  # => co-13 reduce: folds cleaned rows into one Totals


# ---------------------------------------------------------------------------
# Monoid combine + applicative map2 (co-26)
# ---------------------------------------------------------------------------


def combine_totals(
    a: Totals, b: Totals
) -> Totals:  # => the MONOID operation: associative, has an identity
    merged = dict(
        a.by_category
    )  # => starts from a COPY of a -- a itself is never touched
    for (
        category,
        amount,
    ) in b.by_category.items():  # => folds every entry from b onto the copy
        merged[category] = merged.get(category, 0.0) + amount
    return Totals(
        by_category=MappingProxyType(merged)
    )  # => EMPTY_TOTALS is this operation's identity element


def map2(  # => co-26: the applicative combinator -- combines TWO independently-wrapped Results
    fn: Callable[[T, U], V],
    a: "Result[T, tuple[str, ...]]",
    b: "Result[U, tuple[str, ...]]",
) -> "Result[V, tuple[str, ...]]":  # => closes the multi-line signature above
    if isinstance(a, Ok) and isinstance(
        b, Ok
    ):  # => the ONLY case where fn actually runs
        return Ok(
            fn(a.value, b.value)
        )  # => unwraps BOTH, applies fn, wraps the combined result back up
    errors: tuple[
        str, ...
    ] = ()  # => co-26 vs co-24: ACCUMULATES from both sides instead of short-circuiting
    if isinstance(a, Err):  # => a failed -- fold its errors in
        errors += a.error
    if isinstance(
        b, Err
    ):  # => b failed -- fold its errors in TOO, even if a already failed
        errors += b.error
    return Err(
        errors
    )  # => reports every failing side at once, not just the first one found


# ---------------------------------------------------------------------------
# Top-level pure entry points
# ---------------------------------------------------------------------------


def analyze(
    csv_text: str,
) -> "Result[Totals, tuple[str, ...]]":  # => PURE CORE: text in, Result out, no I/O
    lines = csv_text.strip().splitlines()[
        1:
    ]  # => drops the header row, e.g. "category,amount"
    return parse_rows(lines).map(
        aggregate
    )  # => co-25 functor: transforms success, error rides through untouched


def combine_partial_analyses(  # => opens the multi-line signature of the monoid-combine entry point
    csv_text_a: str,
    csv_text_b: str,  # => two independently self-headered "files"
) -> "Result[Totals, tuple[str, ...]]":  # => closes the multi-line signature above
    return map2(
        combine_totals, analyze(csv_text_a), analyze(csv_text_b)
    )  # => co-26 applicative + monoid combine


def top_category(
    totals: Totals,
) -> "Option[str]":  # => co-22: absence is a VALUE, not a None landmine
    if not totals.by_category:  # => nothing was ever aggregated
        return Nothing()
    best = max(
        totals.by_category.items(), key=lambda pair: pair[1]
    )  # => (category, amount) with the max total
    return Some(best[0])


def format_report(totals: Totals) -> str:  # => still PURE: data -> text, zero I/O
    lines = [
        f"{category}: {amount:.2f}"
        for category, amount in sorted(totals.by_category.items())
    ]
    headline = top_category(
        totals
    ).map(  # => co-25 functor: Option.map builds the headline INSIDE the wrapper
        lambda category: f"Top category: {category}"
    )
    if isinstance(headline, Some):  # => a category actually exists
        lines.append(headline.value)
    else:  # => totals.by_category was empty -- top_category() returned Nothing
        lines.append("Top category: (no transactions)")
    return "\n".join(lines)  # => a plain string -- the shell decides how to display it
