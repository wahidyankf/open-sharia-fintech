# learning/code/ex-26-run-it-twice/run_it_twice.py
"""Worked Example 26: Run It Twice."""  # => co-08: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import random  # => co-08: stands in for the model's own internal sampling randomness
import zlib  # => co-08: crc32 gives a STABLE hash across runs -- Python's builtin hash() is randomized per-process for str

CASES = {  # => co-08: four cases -- each entry is (correct phrasing, one flawed phrasing, how often it's flawed)
    "case-01": ("15 GB", "a generous amount", 0.0),  # => co-08: never flaky -- always answers correctly
    "case-02": ("200 GB", "plenty of space", 0.0),  # => co-08: never flaky -- always answers correctly
    "case-08": ("24-hour", "same-day", 0.5),  # => co-08: FLAKY -- roughly half the time it drops the exact figure
    "case-11": ("Pro", "every plan", 0.5),  # => co-08: FLAKY -- roughly half the time it over-generalizes
}  # => co-08: closes CASES


def mock_model_answer(case_id: str, *, seed: int) -> str:  # => co-08: one mocked, seeded call per case
    """Return the correct phrasing unless this seed's roll lands inside this case's flaw rate."""  # => co-08: documents mock_model_answer's contract -- no runtime output, just sets its __doc__
    correct, flawed, flaw_rate = CASES[case_id]  # => co-08: unpack this case's behavior profile
    rng = random.Random(zlib.crc32(f"{case_id}-{seed}".encode()))  # => co-08: reproducible PER (case, seed), varying ACROSS seeds
    return flawed if rng.random() < flaw_rate else correct  # => co-08: the "sample" -- deterministic given case_id and seed


def run_eval(seed: int) -> float:  # => co-07: one full pass over CASES, reduced to a single pass rate
    """Run every case once at this seed and return the resulting pass rate."""  # => co-07: documents run_eval's contract -- no runtime output, just sets its __doc__
    verdicts = [mock_model_answer(cid, seed=seed) == CASES[cid][0] for cid in CASES]  # => co-07: correct-phrasing check per case
    return sum(verdicts) / len(verdicts)  # => co-07: reduce the run to one comparable number


if __name__ == "__main__":  # => co-08: entry point -- runs only when this file executes directly, not on import
    run_1_rate = run_eval(seed=1)  # => co-08: "run 1" of the SAME eval, over the SAME fixed dataset
    run_2_rate = run_eval(seed=2)  # => co-08: "run 2" -- identical setup, a later, independent sampling
    print(f"Run 1 pass rate: {run_1_rate:.2%}")  # => co-08: prints run 1's headline number
    print(f"Run 2 pass rate: {run_2_rate:.2%}")  # => co-08: prints run 2's headline number
    rates_differ = run_1_rate != run_2_rate  # => co-08: the exact symptom co-08 warns about
    print(f"Pass rates differ across runs: {rates_differ}")  # => co-08: True -- a single run's number is not yet evidence
    assert rates_differ, "two runs of a stochastic eval must NOT always land on the same pass rate"  # => co-08
    print("MATCH: a single run's pass rate is a sample, not a certainty -- re-running is the cheapest check available")  # => co-08
    # => co-08: never accept or reject a change on ONE run's number alone -- ex-27 and ex-28 build on exactly this
