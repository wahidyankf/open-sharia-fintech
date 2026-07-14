"""Capstone: app.__main__ -- the argparse CLI entry point (`python3 -m app`).

Reads an inventory JSON file, validates and summarizes it via app.transform, then
writes and prints the resulting summary JSON. A validation failure is caught here
and reported as a clean one-line message with a non-zero exit code, never a raw
traceback -- the CLI's whole job is translating transform.py's exceptions into
something a terminal user can act on.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# A cross-module import within the SAME package (Example 64's shape).
from app.transform import (
    InvalidRecordError,
    InventoryRecord,
    grand_total,
    summarize,
    validate_records,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Summarize an inventory JSON file's total value per item."
    )
    parser.add_argument("input", type=str, help="path to the input inventory JSON file")
    parser.add_argument("output", type=str, help="path to write the summary JSON file")
    # Example 61's argparse pattern, with two positionals instead of one.
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    # `with` guarantees the file closes (Example 52's pattern).
    with input_path.open() as f:
        # Example 58's json.load pattern -- reads the whole file as one JSON value.
        records: list[InventoryRecord] = json.load(f)

    try:
        validate_records(records)
    except InvalidRecordError as err:
        # Example 65's custom-exception-class pattern: a clean message, not a raw traceback.
        print(f"invalid inventory data: {err}", file=sys.stderr)
        sys.exit(1)  # a distinct, deliberate non-zero exit code for bad input

    summary = summarize(records)
    payload = {"items": summary, "grand_total": grand_total(summary)}

    with output_path.open("w") as f:
        json.dump(payload, f)  # Example 57's json.dump-to-file pattern

    # Echoes the same payload to stdout for the caller to see.
    print(json.dumps(payload))


# Example 46's guard -- app.__main__ only runs main() when invoked directly
# (e.g. via `python3 -m app`), never when merely imported.
if __name__ == "__main__":
    main()
