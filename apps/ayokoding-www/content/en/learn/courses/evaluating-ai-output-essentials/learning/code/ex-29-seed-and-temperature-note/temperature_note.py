# learning/code/ex-29-seed-and-temperature-note/temperature_note.py
"""Worked Example 29: Seed-and-Temperature Note."""  # => co-08: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import random  # => co-08: stands in for the model's own internal sampling randomness

BASE_FLAW_RATE = 0.5  # => co-08: this case's flaw rate at maximum sampling temperature (temperature = 1.0)
TRIAL_COUNT = 200  # => co-08: enough trials that a rate near zero is still distinguishable from truly zero


def flips_at_temperature(temperature: float, *, trials: int) -> int:  # => co-08: counts flawed outputs at a given temperature
    """Run `trials` mocked calls at `temperature` and count how many produced the flawed answer."""  # => co-08: documents flips_at_temperature's contract -- no runtime output, just sets its __doc__
    effective_flaw_rate = BASE_FLAW_RATE * temperature  # => co-08: lower temperature scales the flaw rate DOWN, not to zero
    rng = random.Random(7)  # => co-08: one fixed seed reused across BOTH temperatures -- isolates temperature as the only variable
    return sum(1 for _ in range(trials) if rng.random() < effective_flaw_rate)  # => co-08: count trials that landed on "flawed"


if __name__ == "__main__":  # => co-08: entry point -- runs only when this file executes directly, not on import
    high_temp_flips = flips_at_temperature(temperature=1.0, trials=TRIAL_COUNT)  # => co-08: high temperature -- maximal variance
    low_temp_flips = flips_at_temperature(temperature=0.1, trials=TRIAL_COUNT)  # => co-08: low temperature -- reduced variance
    print(f"High temperature (1.0): {high_temp_flips}/{TRIAL_COUNT} flawed outputs")  # => co-08: prints the high-temp count
    print(f"Low temperature (0.1): {low_temp_flips}/{TRIAL_COUNT} flawed outputs")  # => co-08: prints the low-temp count
    assert low_temp_flips < high_temp_flips, "lowering temperature must reduce the flip count"  # => co-08: confirms the reduction
    assert low_temp_flips > 0, "lowering temperature must NOT drive the flip count to exactly zero"  # => co-08: confirms the caveat
    print("MATCH: lower temperature reduces variance, but 0.1 is not 0.0 -- some flips remain")  # => co-08
    # => co-08: "we lowered the temperature" is not a substitute for run-it-twice -- it shrinks the risk, it does not remove it
