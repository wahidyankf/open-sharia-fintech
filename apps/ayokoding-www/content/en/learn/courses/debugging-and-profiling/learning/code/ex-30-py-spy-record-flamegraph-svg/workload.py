"""Example 30: the workload this example's real flame graph SVG was sampled from."""

from __future__ import annotations


def validate_row(row: dict[str, str]) -> bool:
    return "id" in row and "name" in row


def clean_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [row for row in rows if validate_row(row)]


def run_workload() -> None:
    rows = [{"id": str(i), "name": f"item{i}"} for i in range(30_000)]
    for _ in range(120):
        clean_rows(rows)
