# learning/code/ex-09-ten-cases-is-not-coverage/coverage_limits.py
"""Worked Example 9: Ten Cases Is Not Coverage."""  # => co-03: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import json  # => co-03: JSONL needs nothing beyond the standard library's own json module
from pathlib import Path  # => co-03: locates dataset.jsonl relative to this script, not the caller's cwd

DATASET_PATH = Path(__file__).parent / "dataset.jsonl"  # => co-03: the same ten-case gate ex-05 built
ALL_KNOWN_PRODUCT_FACTS = {  # => co-12: every fact a real support team actually fields questions about
    "storage-free",  # => co-12: fact 1 -- covered
    "storage-pro",  # => co-12: fact 2 -- covered
    "security-2fa",  # => co-12: fact 3 -- covered
    "platforms",  # => co-12: fact 4 -- covered
    "file-size-free",  # => co-12: fact 5 -- covered
    "file-size-pro",  # => co-12: fact 6 -- covered
    "share-link-expiry",  # => co-12: fact 7 -- covered
    "support-response",  # => co-12: fact 8 -- covered
    "trash-retention",  # => co-12: fact 9 -- covered
    "offline-sync",  # => co-12: fact 10 -- covered, ten total
    "api-access",  # => co-12: fact 11 -- NEVER tested
    "encryption",  # => co-12: fact 12 -- NEVER tested
    "password-reset",  # => co-12: fact 13 -- NEVER tested
    "team-sharing",  # => co-12: fact 14 -- NEVER tested
    "audit-log",  # => co-12: fact 15 -- NEVER tested
    "sso-support",  # => co-12: fact 16 -- NEVER tested
}  # => co-12: closes the known-facts set -- sixteen facts a support team actually fields


def load_fact_ids(path: Path) -> set[str]:  # => co-03: which facts does the committed dataset actually exercise?
    """Return the set of fact_id values the dataset's cases cover."""  # => co-03: documents load_fact_ids's contract -- no runtime output, just sets its __doc__
    return {  # => co-03: a set comprehension -- duplicate coverage of the same fact would still count once
        json.loads(line)["fact_id"]  # => co-03: pull just the fact_id field out of each parsed case
        for line in path.read_text(encoding="utf-8").splitlines()  # => co-03: one JSON object per non-blank line
        if line.strip()  # => co-03: skip any stray blank line without raising
    }  # => co-03: closes the set comprehension


if __name__ == "__main__":  # => co-03: entry point -- runs only when this file executes directly, not on import
    covered = load_fact_ids(DATASET_PATH)  # => co-03: what the ten-case dataset actually tests
    uncovered = ALL_KNOWN_PRODUCT_FACTS - covered  # => co-12: what it provably does NOT test
    print(f"Dataset covers {len(covered)}/{len(ALL_KNOWN_PRODUCT_FACTS)} known facts")  # => co-12: the honest ratio
    print(f"Never tested: {sorted(uncovered)}")  # => co-12: exactly which facts a green run says nothing about
    assert len(covered) == 10, "this dataset must cover exactly ten facts"  # => co-03: sanity check on the fixture
    assert uncovered == {  # => co-12: the exact six facts this gate is silent on
        "api-access",  # => co-12: uncovered 1
        "encryption",  # => co-12: uncovered 2
        "password-reset",  # => co-12: uncovered 3
        "team-sharing",  # => co-12: uncovered 4
        "audit-log",  # => co-12: uncovered 5
        "sso-support",  # => co-12: uncovered 6
    }, "the uncovered set must be exactly the six facts this dataset never touches"  # => co-12
    print("A green run over these ten cases proves nothing about the six facts above")  # => co-12: the honest limit
    # => co-12: recognising what a small fixed set does NOT cover is what keeps a green run from becoming false confidence
