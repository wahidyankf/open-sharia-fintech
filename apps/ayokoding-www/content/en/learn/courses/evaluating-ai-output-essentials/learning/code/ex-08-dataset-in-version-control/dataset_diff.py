# learning/code/ex-08-dataset-in-version-control/dataset_diff.py
"""Worked Example 8: Dataset in Version Control."""  # => co-03: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import json  # => co-03: JSONL needs nothing beyond the standard library's own json module
from pathlib import Path  # => co-03: locates both dataset commits relative to this script, not the caller's cwd

V1_PATH = Path(__file__).parent / "dataset_v1.jsonl"  # => co-03: "commit 1" -- three cases, the dataset's first version
V2_PATH = Path(__file__).parent / "dataset_v2.jsonl"  # => co-03: "commit 2" -- the same repo file, one commit later


def load_ids(path: Path) -> set[str]:  # => co-03: reduces a dataset commit to just its set of case ids
    """Load a JSONL dataset commit and return only its set of case ids."""  # => co-03: documents load_ids's contract -- no runtime output, just sets its __doc__
    return {  # => co-03: a set comprehension -- id order does not matter for a diff, only membership
        json.loads(line)["id"]  # => co-03: pull just the id field out of each parsed case
        for line in path.read_text(encoding="utf-8").splitlines()  # => co-03: one JSON object per non-blank line
        if line.strip()  # => co-03: skip any stray blank line without raising
    }  # => co-03: closes the set comprehension


if __name__ == "__main__":  # => co-03: entry point -- runs only when this file executes directly, not on import
    v1_ids = load_ids(V1_PATH)  # => co-03: the case ids present at commit 1
    v2_ids = load_ids(V2_PATH)  # => co-03: the case ids present at commit 2
    print(f"Commit 1 case ids: {sorted(v1_ids)}")  # => co-03: prints commit 1's exact case set
    print(f"Commit 2 case ids: {sorted(v2_ids)}")  # => co-03: prints commit 2's exact case set

    added = v2_ids - v1_ids  # => co-03: present in commit 2, absent from commit 1 -- exactly what a git diff would show
    removed = v1_ids - v2_ids  # => co-03: present in commit 1, absent from commit 2
    unchanged = v1_ids & v2_ids  # => co-03: present in both -- the stable core neither commit touched
    print(f"Added: {sorted(added)}")  # => co-03: prints exactly which cases the second commit introduced
    print(f"Removed: {sorted(removed)}")  # => co-03: prints exactly which cases the second commit dropped, if any
    print(f"Unchanged: {sorted(unchanged)}")  # => co-03: prints the cases both commits agree on

    assert added == {"case-04", "case-13"}, "commit 2 must add exactly case-04 and case-13"  # => co-03: the exact expected diff
    assert removed == set(), "commit 2 must remove no case in this scenario"  # => co-03: a pure, additive evolution
    print(f"MATCH: the diff shows exactly {sorted(added)} were added, nothing removed")  # => co-03: reached only if both asserts passed
    # => co-03: a versioned JSONL file makes "what changed in this eval?" as answerable as "what changed in this code?"
