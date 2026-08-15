"""Small, local teaching artefact for a reviewable take-home submission."""

from __future__ import annotations

import sys
from collections.abc import Iterable
from pathlib import Path


class RecordError(ValueError):
    """A record does not satisfy the deliberately small line-format contract."""


def parse_record(line: str, line_number: int) -> tuple[str, int]:
    """Return one validated owner/count pair or a message a caller can act on."""

    pieces = line.rstrip("\n").split(",")
    if len(pieces) != 2:
        raise RecordError(f"line {line_number}: expected owner,count")
    owner = pieces[0].strip()
    if not owner:
        raise RecordError(f"line {line_number}: owner must not be blank")
    try:
        count = int(pieces[1].strip())
    except ValueError as error:
        raise RecordError(f"line {line_number}: count must be an integer") from error
    if count < 0:
        raise RecordError(f"line {line_number}: count must be a non-negative integer")
    return owner, count


def summarize(lines: Iterable[str]) -> dict[str, int]:
    """Aggregate valid records; blank lines are not records and are ignored."""

    totals: dict[str, int] = {}
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        owner, count = parse_record(line, line_number)
        totals[owner] = totals.get(owner, 0) + count
    return totals


def render(totals: dict[str, int]) -> str:
    """Render deterministic, line-oriented output for a reviewer and test."""

    return "\n".join(f"{owner}: {totals[owner]}" for owner in sorted(totals))


def read_and_summarize(path: Path) -> str:
    """Open the supplied local file and return its formatted summary."""

    return render(summarize(path.read_text(encoding="utf-8").splitlines(keepends=True)))


def main(arguments: list[str]) -> int:
    """Run the CLI without hiding file or validation failures."""

    if len(arguments) != 1:
        print("usage: python briefcheck.py RECORDS_FILE", file=sys.stderr)
        return 2
    try:
        result = read_and_summarize(Path(arguments[0]))
    except (OSError, RecordError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    if result:
        print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
