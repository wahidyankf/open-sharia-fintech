"""Recovery replays only committed complete records."""

from __future__ import annotations

from pathlib import Path

from wal import records


def committed_rows(path: Path) -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    for record in records(path):
        if record.get("kind") == "commit":
            row = record["row"]
            assert isinstance(row, dict)
            parsed = {str(key): str(value) for key, value in row.items()}
            rows[parsed["id"]] = parsed
    return rows
