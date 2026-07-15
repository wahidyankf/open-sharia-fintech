"""Example 17: First cProfile Run from the Command Line."""

from __future__ import annotations


def slow_format_row(row: dict[str, float]) -> str:
    return ", ".join(f"{k}={v:.2f}" for k, v in sorted(row.items()))


def build_report(rows: list[dict[str, float]]) -> list[str]:
    return [slow_format_row(row) for row in rows]


def compute_total(rows: list[dict[str, float]]) -> float:
    total = 0.0
    for row in rows:
        for v in row.values():
            total += v
    return total


if __name__ == "__main__":
    data = [{"a": i * 1.5, "b": i * 2.5, "c": i * 0.5} for i in range(20_000)]
    report = build_report(data)
    total = compute_total(data)
    print(f"rows={len(report)} total={total:.2f}")
