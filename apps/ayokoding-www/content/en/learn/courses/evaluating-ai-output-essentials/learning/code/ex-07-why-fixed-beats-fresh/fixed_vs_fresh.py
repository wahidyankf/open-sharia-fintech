# learning/code/ex-07-why-fixed-beats-fresh/fixed_vs_fresh.py
"""Worked Example 7: Why Fixed Beats Fresh."""  # => co-03: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import random  # => co-03: generates the "fresh" random inputs each run

FIXED_SET = ["storage-free", "storage-pro", "security-2fa", "encryption"]  # => co-03: the SAME four fact-ids, every single run
FACT_POOL = [  # => co-03: the pool a "fresh" sampler draws from -- larger than what any one run uses
    "storage-free",  # => co-03: pool entry 1
    "storage-pro",  # => co-03: pool entry 2
    "security-2fa",  # => co-03: pool entry 3
    "encryption",  # => co-03: pool entry 4
    "platforms",  # => co-03: pool entry 5
    "file-size-free",  # => co-03: pool entry 6
    "file-size-pro",  # => co-03: pool entry 7
    "share-link-expiry",  # => co-03: pool entry 8
]  # => co-03: closes the pool list


def fresh_sample(seed: int, size: int = 4) -> list[str]:  # => co-03: a NEW random subset, drawn independently each run
    """Draw `size` fact-ids at random from FACT_POOL -- a fresh sample, not a fixed one."""  # => co-03: documents fresh_sample's contract -- no runtime output, just sets its __doc__
    return random.Random(seed).sample(FACT_POOL, size)  # => co-03: a different seed stands in for "run again, later"


if __name__ == "__main__":  # => co-03: entry point -- runs only when this file executes directly, not on import
    fixed_run_1 = list(FIXED_SET)  # => co-03: "run 1" against the fixed set -- literally the same list object's contents
    fixed_run_2 = list(FIXED_SET)  # => co-03: "run 2" against the fixed set -- unchanged, because it's fixed
    print(f"Fixed set, run 1: {fixed_run_1}")  # => co-03: prints run 1's exact case set
    print(f"Fixed set, run 2: {fixed_run_2}")  # => co-03: prints run 2's exact case set
    fixed_overlap = set(fixed_run_1) & set(fixed_run_2)  # => co-03: how much the two runs actually share
    print(f"Fixed-set overlap: {len(fixed_overlap)}/{len(FIXED_SET)}")  # => co-03: 4/4 -- fully comparable

    fresh_run_1 = fresh_sample(seed=1)  # => co-03: "run 1" against a fresh sample
    fresh_run_2 = fresh_sample(seed=2)  # => co-03: "run 2" against a DIFFERENT fresh sample -- a later, unrelated draw
    print(f"Fresh sample, run 1: {fresh_run_1}")  # => co-03: prints run 1's fresh case set
    print(f"Fresh sample, run 2: {fresh_run_2}")  # => co-03: prints run 2's fresh case set
    fresh_overlap = set(fresh_run_1) & set(fresh_run_2)  # => co-03: how much the two fresh runs actually share
    print(f"Fresh-sample overlap: {len(fresh_overlap)}/{len(FIXED_SET)}")  # => co-03: less than 4/4 -- NOT comparable

    assert len(fixed_overlap) == len(FIXED_SET), "the fixed set must overlap itself completely, every run"  # => co-03
    assert len(fresh_overlap) < len(FIXED_SET), "two independent fresh samples must NOT fully overlap"  # => co-03
    print("Only the fixed set supports a before/after comparison across runs")  # => co-03: the point of ex-07
    # => co-03: co-09's whole comparison only means something once BOTH runs measured the SAME cases
