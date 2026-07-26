# learning/code/ex-27-flaky-case-detection/flaky_case_detection.py
"""Worked Example 27: Flaky-Case Detection."""  # => co-08: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import random  # => co-08: stands in for the model's own internal sampling randomness
import zlib  # => co-08: crc32 gives a STABLE hash across runs -- Python's builtin hash() is randomized per-process for str

CASES = {  # => co-08: three cases -- two rock-solid, one genuinely flaky
    "case-01": ("15 GB", "a generous amount", 0.0),  # => co-08: never flaky
    "case-08": ("24-hour", "same-day", 0.5),  # => co-08: FLAKY -- flips roughly half the time
    "case-12": ("AES-256", "strong encryption", 0.0),  # => co-08: never flaky
}  # => co-08: closes CASES
TRIAL_COUNT = 5  # => co-08: five repeat trials -- cheap, and enough to expose a 50% flip rate


def mock_model_answer(case_id: str, *, trial: int) -> str:  # => co-08: one mocked, seeded call per (case, trial)
    """Return the correct phrasing unless this trial's roll lands inside this case's flaw rate."""  # => co-08: documents mock_model_answer's contract -- no runtime output, just sets its __doc__
    correct, flawed, flaw_rate = CASES[case_id]  # => co-08: unpack this case's behavior profile
    rng = random.Random(zlib.crc32(f"{case_id}-{trial}".encode()))  # => co-08: reproducible PER (case, trial), varying ACROSS trials
    return flawed if rng.random() < flaw_rate else correct  # => co-08: the "sample" for this specific trial


if __name__ == "__main__":  # => co-08: entry point -- runs only when this file executes directly, not on import
    verdicts_by_case: dict[str, list[bool]] = {cid: [] for cid in CASES}  # => co-08: accumulates every trial's verdict, per case
    for trial in range(TRIAL_COUNT):  # => co-08: repeat the SAME cases TRIAL_COUNT times
        for case_id in CASES:  # => co-08: one call per case, per trial
            correct_phrasing = CASES[case_id][0]  # => co-08: this case's own correct phrasing
            output = mock_model_answer(case_id, trial=trial)  # => co-08: this trial's sampled answer
            verdicts_by_case[case_id].append(output == correct_phrasing)  # => co-08: record this trial's pass/fail

    print(f"Verdicts across {TRIAL_COUNT} trials:")  # => co-08: states the trial count up front
    flaky_cases: list[str] = []  # => co-08: accumulates every case whose verdict flips at least once
    for case_id, verdicts in verdicts_by_case.items():  # => co-08: inspect each case's own trial-by-trial history
        print(f"  {case_id}: {verdicts}")  # => co-08: prints the raw per-trial verdict list
        is_flaky = len(set(verdicts)) > 1  # => co-08: flaky iff BOTH True and False appear across the trials
        if is_flaky:  # => co-08: only cases that actually flipped get flagged
            flaky_cases.append(case_id)  # => co-08: record this case as flaky
    print(f"Flaky cases: {flaky_cases}")  # => co-08: prints exactly which cases need n-of-k handling (ex-28)
    assert flaky_cases == ["case-08"], "exactly the deliberately-flaky case must be flagged"  # => co-08
    print("MATCH: repeat trials expose exactly the one case whose verdict is not yet reliable")  # => co-08
    # => co-08: a case that flips across identical trials is telling you something the single-run pass rate hid
