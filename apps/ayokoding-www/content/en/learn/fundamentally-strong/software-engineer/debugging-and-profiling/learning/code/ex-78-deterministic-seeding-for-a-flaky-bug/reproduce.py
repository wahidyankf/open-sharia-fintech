"""Example 78: show a ~1-in-20 flaky bug (unseeded), then a DETERMINISTIC
reproduction of that SAME rare outcome on every single run once the seed is pinned.
"""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the reproduction itself

import sys  # => needed only for sys.path.insert below

sys.path.insert(
    0, "."
)  # => makes local flaky_target.py importable regardless of caller's cwd
from flaky_target import run_once  # noqa: E402  # => co-20/co-07: the SAME flaky function this whole example reproduces


def main() -> (
    None
):  # => co-20/co-07: shows the natural flake rate, finds a reproducing seed, then confirms determinism
    print(
        "=== UNSEEDED: the rare 'B wins' outcome shows up unpredictably, roughly 1-in-20 ==="
    )  # => co-20: names this phase
    results_unseeded = [
        run_once(seed=None) for _ in range(60)
    ]  # => co-20: 60 genuinely unseeded attempts -- real randomness
    b_count = results_unseeded.count(
        "B"
    )  # => co-20: counts how many of the 60 landed on the rare "B" outcome
    print(
        f"'B' wins in {b_count}/60 unseeded runs (roughly the expected ~1-in-20 rate)"
    )  # => co-20: the observed real rate
    assert 0 < b_count < 60, (
        "expected the unseeded runs to show BOTH outcomes across 60 tries"
    )  # => co-20: sanity check on real randomness

    print()  # => co-07: a blank line, separating the UNSEEDED phase from the SEED-SEARCH phase below
    print(
        "=== find a seed that reproduces the RARE 'B wins' outcome ==="
    )  # => co-07: names this phase
    reproducing_seed = None  # => co-07: filled in by the search loop below, once a matching seed is found
    for candidate_seed in range(
        1000
    ):  # => co-07: searches a fixed, small range -- deterministic, not open-ended
        if (
            run_once(seed=candidate_seed) == "B"
        ):  # => co-07: tests each candidate seed for the RARE outcome specifically
            reproducing_seed = candidate_seed  # => co-07: keeps the FIRST seed found that reproduces "B wins"
            break  # => co-07: stops searching once one reproducing seed is found -- no need to keep looking
    assert reproducing_seed is not None, (
        "expected at least one seed in [0, 1000) to reproduce 'B wins'"
    )  # => co-07: the real check
    print(
        f"seed={reproducing_seed} reproduces the rare outcome"
    )  # => co-07: names the specific seed found

    print()  # => co-07: a blank line, separating the SEED-SEARCH phase from the SEEDED phase below
    print(
        f"=== SEEDED (seed={reproducing_seed}): reproduces on EVERY local run ==="
    )  # => co-07: names the final phase
    results_seeded = [
        run_once(seed=reproducing_seed) for _ in range(20)
    ]  # => co-07: 20 runs, ALL using the SAME pinned seed
    print(
        f"owners across 20 runs with the pinned seed: {results_seeded}"
    )  # => co-07: shows every single outcome, for inspection
    assert set(results_seeded) == {"B"}, (
        "expected the pinned seed to reproduce 'B wins' on every single run"
    )  # => co-07: the real check
    print(
        "confirmed: the ~1-in-20 failure now reproduces on every local run with the seed pinned"
    )  # => co-07/co-20: the payoff


if (
    __name__ == "__main__"
):  # => guards the module-level call so importing this file stays side-effect-free
    main()  # => the one call that shows the flake rate, finds a seed, and confirms determinism
