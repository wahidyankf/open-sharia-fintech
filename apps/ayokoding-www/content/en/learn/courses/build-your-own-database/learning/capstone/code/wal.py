"""Append-only JSON-line WAL records with an fsync commit boundary."""

from __future__ import annotations

import json
import os
from pathlib import Path


def append(path: Path, record: dict[str, object]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def records(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        return []
    complete: list[dict[str, object]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            complete.append(json.loads(line))
        except json.JSONDecodeError:
            break
    return complete
