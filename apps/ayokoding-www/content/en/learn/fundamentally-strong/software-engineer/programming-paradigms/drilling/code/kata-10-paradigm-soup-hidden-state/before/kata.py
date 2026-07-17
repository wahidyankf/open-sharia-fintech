"""Kata 10 (before): paradigm-soup violation -- a `map`-based pipeline secretly mutates shared MODULE state."""

from typing import cast

_seen_ids: list[int] = []  # SMELL: module-level mutable state captured by a "functional-looking" map


def enrich(row: dict[str, object]) -> dict[str, object]:
    _seen_ids.append(cast(int, row["id"]))  # BUG: side effect hidden inside what looks like a pure transform
    return {"id": row["id"], "seen_count": len(_seen_ids)}


def build_report(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return list(map(enrich, rows))


rows: list[dict[str, object]] = [{"id": 1}, {"id": 2}]
report_a = build_report(rows)
report_b = build_report(rows)  # same input, called again
print([r["seen_count"] for r in report_a])
print([r["seen_count"] for r in report_b])  # BUG: NOT equal to report_a -- proves it's not referentially transparent
