"""Capstone step 4: fix the hot spot (dedupe_customers, O(n^2) -> O(n)), then
re-measure with a documented before/after speedup and confirm zero test
regressions.
"""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the measurement itself

import subprocess  # => co-23: runs the REAL regression-test suite as a subprocess -- not a mocked assertion
import sys  # => co-23: sys.executable -- runs the SAME interpreter this script itself is running under
import time  # => co-23: time.perf_counter() -- measures REAL wall time, before and after the fix

sys.path.insert(
    0, "."
)  # => makes local make_large_batch.py importable regardless of caller's cwd
from make_large_batch import make_large_batch  # noqa: E402  # => co-23: the SAME large batch step 3's profiles both used


def timed_report(
    orders: list[dict],
) -> (
    float
):  # => co-23: times ONE full pipeline run, reloading pipeline.py fresh each call
    import importlib  # => co-23: importlib.reload() -- forces pipeline.py's ON-DISK content to be re-read, not cached

    import pipeline  # => co-23: imported HERE, not at module level, so reload() always sees the CURRENT file on disk

    importlib.reload(
        pipeline
    )  # => co-23: re-reads pipeline.py from disk -- picks up the fix applied between calls below
    start = time.perf_counter()  # => co-23: starts timing BEFORE the pipeline call
    pipeline.build_customer_report(
        orders
    )  # => co-23: the SAME batch, run through whichever version is on disk right now
    return (
        time.perf_counter() - start
    )  # => co-23: the REAL wall time for this ONE pipeline run


def main() -> (
    None
):  # => co-23: measures BEFORE, applies the fix, measures AFTER, and confirms zero test regressions
    orders = (
        make_large_batch()
    )  # => co-23: the SAME 60,000-order batch used by both profiling steps above

    before = timed_report(
        orders
    )  # => co-23: the O(n^2) dedupe's real wall time, on this exact batch
    print(
        f"BEFORE (O(n^2) dedupe): {before * 1000:.1f}ms"
    )  # => co-23: the BEFORE number, for the final comparison

    # co-23: apply the fix -- read from disk to keep this measurement honest
    # (the SAME file the regression tests import from, not an in-memory patch).
    with (
        open("pipeline.py") as f
    ):  # => co-23: reads the CURRENT on-disk pipeline.py -- the same file test_pipeline.py imports
        original_source = (
            f.read()
        )  # => co-23: the exact current source text, byte for byte
    fixed_source = original_source.replace(  # => co-23: a targeted, exact-text replacement -- not a hand-rewritten file
        "    seen: list[str] = []\n"  # => co-23: OLD line 1 -- the O(n)-membership LIST this fix replaces
        "    result: list[dict] = []\n"  # => co-23: OLD line 2 -- unchanged in the fix, kept for an exact-text match
        "    for order in orders:\n"  # => co-23: OLD line 3 -- the SAME loop shape survives into the fixed version
        '        customer_id = order["customer_id"]\n'  # => co-23: OLD line 4 -- unchanged, same field read both versions
        "        if customer_id not in seen:\n"  # => co-23: OLD line 5 -- the O(n) list "in" check this fix targets
        "            seen.append(customer_id)\n"  # => co-23: OLD line 6 -- becomes seen.add() in the fixed body below
        "            result.append(order)\n"  # => co-23: OLD line 7 -- unchanged, same output-building step
        "    return result",  # => co-23: OLD line 8 -- closes the OLD body; this whole 8-line block is matched verbatim
        "    # FIX (performance): O(1) set-membership check instead of O(n) list scan.\n"  # => co-23: NEW line 0 -- the fix's own comment
        "    seen: set[str] = set()\n"  # => co-23: NEW line 1 -- O(1)-membership SET, replacing the OLD list
        "    result: list[dict] = []\n"  # => co-23: NEW line 2 -- identical to the OLD version's own line 2
        "    for order in orders:\n"  # => co-23: NEW line 3 -- identical to the OLD version's own line 3
        '        customer_id = order["customer_id"]\n'  # => co-23: NEW line 4 -- identical to the OLD version's own line 4
        "        if customer_id not in seen:\n"  # => co-23: NEW line 5 -- now an O(1) set lookup, not an O(n) list scan
        "            seen.add(customer_id)\n"  # => co-23: NEW line 6 -- the actual fix, replacing seen.append()
        "            result.append(order)\n"  # => co-23: NEW line 7 -- identical to the OLD version's own line 7
        "    return result",  # => co-23: NEW line 8 -- closes the fixed body; SAME output shape as the OLD version
    )  # => co-23: closes the replace() call -- fixed_source now has the O(n) version, byte-identical elsewhere
    assert fixed_source != original_source, (
        "the fix replacement did not match -- check pipeline.py's exact text"
    )  # => co-23: real check
    with (
        open("pipeline.py", "w") as f
    ):  # => co-23: writes the fixed version BACK to disk -- the same file test_pipeline.py imports
        f.write(
            fixed_source
        )  # => co-23: persists the fix -- the next timed_report() call reloads THIS content

    after = timed_report(
        orders
    )  # => co-23: the O(n) dedupe's real wall time, on the IDENTICAL batch
    print(
        f"AFTER  (O(n) dedupe):   {after * 1000:.1f}ms"
    )  # => co-23: the AFTER number, for the final comparison

    speedup = (
        before / after
    )  # => co-23: how many TIMES faster the fix made this specific batch's pipeline run
    print(
        f"speedup: {speedup:.1f}x"
    )  # => co-23: the headline result -- a documented, quantified improvement
    assert after < before, (
        "expected the fix to be measurably faster"
    )  # => co-23: the real, quantified check

    print()  # => co-23: a blank line, separating the speedup report from the regression-check phase below
    print(
        "$ python3 -m pytest -q test_pipeline.py   (confirm zero regressions)"
    )  # => co-23: names the final phase
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "test_pipeline.py"],
        capture_output=True,
        text=True,
    )  # => co-23
    print(
        result.stdout
    )  # => co-23: shows pytest's own real output -- not a mocked "tests passed" message
    assert result.returncode == 0, (
        "expected all regression tests to still pass after the performance fix"
    )  # => co-23: real check
    print(
        f"confirmed: {speedup:.1f}x speedup with zero test regressions"
    )  # => co-23: the capstone's final, combined claim


if (
    __name__ == "__main__"
):  # => guards the module-level call so importing this file stays side-effect-free
    main()  # => the one call that measures, fixes, re-measures, and confirms zero regressions
