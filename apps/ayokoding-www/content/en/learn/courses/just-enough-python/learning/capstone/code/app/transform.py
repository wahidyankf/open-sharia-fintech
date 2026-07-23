"""Capstone: pure transform functions -- validate and summarize inventory records.

No file I/O and no argparse here on purpose: every function in this module is pure,
which is exactly what makes it trivially unit-testable in tests/test_transform.py
without touching a filesystem or a CLI.
"""

from __future__ import annotations

from typing import TypedDict


class InvalidRecordError(Exception):
    """Raised when an inventory record fails validation."""


class InventoryRecord(TypedDict):
    """One row of the input JSON: an item name, its count, and its unit price."""

    name: str
    quantity: int
    price: float


class SummaryRecord(TypedDict):
    """One row of the output JSON: the item name plus its computed total value."""

    name: str
    quantity: int
    total_value: float


def validate_records(records: list[InventoryRecord]) -> list[InventoryRecord]:
    """Reject any record with a negative quantity or price.

    Raising a custom, named exception (rather than a bare ValueError) lets the CLI
    layer catch exactly this failure mode and print a clean message instead of a
    raw traceback -- the same distinction Example 65 draws in the learning track.
    """
    for record in records:  # => a plain for loop -- fails fast on the FIRST bad record
        if record["quantity"] < 0:
            raise InvalidRecordError(f"{record['name']!r} has a negative quantity")
        if record["price"] < 0:
            raise InvalidRecordError(f"{record['name']!r} has a negative price")
    return records  # => unchanged -- this function validates, it never mutates


def summarize(records: list[InventoryRecord]) -> list[SummaryRecord]:
    """Compute each record's total value (quantity * price) via a comprehension."""
    return [
        {
            "name": record["name"],
            "quantity": record["quantity"],
            "total_value": round(record["quantity"] * record["price"], 2),
            # => round(..., 2) keeps prices display-friendly -- Example 6's float lesson, applied
        }
        for record in records  # => one comprehension replaces a build-up loop (Example 29's pattern)
    ]


def grand_total(summary: list[SummaryRecord]) -> float:
    """Sum every summary row's total_value -- a generator expression, not a loop."""
    return round(sum(row["total_value"] for row in summary), 2)
    # => sum(... for ...) is Example 33's generator-expression pattern, not a materialized list
