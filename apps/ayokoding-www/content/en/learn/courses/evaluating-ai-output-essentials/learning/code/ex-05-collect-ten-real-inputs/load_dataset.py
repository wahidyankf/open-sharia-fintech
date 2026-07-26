# learning/code/ex-05-collect-ten-real-inputs/load_dataset.py
"""Worked Example 5: Collect Ten Real Inputs."""  # => co-03: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import json  # => co-03: JSONL needs nothing beyond the standard library's own json module
from pathlib import Path  # => co-03: locates dataset.jsonl relative to this script, not the caller's cwd

DATASET_PATH = Path(__file__).parent / "dataset.jsonl"  # => co-03: colocated, versioned, and committed alongside this file


def load_dataset(path: Path) -> list[dict[str, str]]:  # => co-03: one JSON object per line -> one case dict per line
    """Load a JSONL dataset file into a list of case dicts, one dict per non-blank line."""  # => co-03: documents load_dataset's contract -- no runtime output, just sets its __doc__
    cases: list[dict[str, str]] = []  # => co-03: accumulates one parsed case per line
    for line in path.read_text(encoding="utf-8").splitlines():  # => co-03: splitlines -- JSONL is newline-delimited, not one big array
        if line.strip():  # => co-03: skip any stray blank line without raising
            cases.append(json.loads(line))  # => co-03: each line is independently valid JSON
    return cases  # => co-03: returns this computed value to the caller


if __name__ == "__main__":  # => co-03: entry point -- runs only when this file executes directly, not on import
    cases = load_dataset(DATASET_PATH)  # => co-03: the whole point -- this file is committed, so this call is reproducible
    print(f"Loaded {len(cases)} cases from {DATASET_PATH.name}")  # => co-03: prints the count actually on disk
    for case in cases:  # => co-03: one line of output per case, for a quick visual sanity check
        print(f"  {case['id']}: {case['input']}")  # => co-03: shows id + input for every case
    assert len(cases) >= 10, "the dataset must have at least ten cases"  # => co-03: the floor this worked example demonstrates
    unique_ids = {case["id"] for case in cases}  # => co-03: every case must be independently addressable
    assert len(unique_ids) == len(cases), "every case id must be unique"  # => co-03: no silent duplicate case
    print(f"MATCH: {len(cases)} committed, loadable, uniquely-identified cases")  # => co-03: reached only if both asserts passed
    # => co-03: the fixed-ness of this file -- not its size -- is what makes it a gate, not a vibe check
