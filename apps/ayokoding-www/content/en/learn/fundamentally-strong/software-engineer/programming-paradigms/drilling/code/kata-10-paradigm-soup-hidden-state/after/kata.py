"""Kata 10 (after): paradigm-soup fix -- the transform depends ONLY on its own arguments, no shared state."""


def enrich(row: dict[str, object], index: int) -> dict[str, object]:
    return {"id": row["id"], "seen_count": index + 1}  # depends only on its OWN inputs -- no closure, no shared list


def build_report(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [enrich(row, i) for i, row in enumerate(rows)]  # pure -- same input always produces same output


rows: list[dict[str, object]] = [{"id": 1}, {"id": 2}]
report_a = build_report(rows)
report_b = build_report(rows)
print([r["seen_count"] for r in report_a])
print([r["seen_count"] for r in report_b])  # now IDENTICAL -- referentially transparent
