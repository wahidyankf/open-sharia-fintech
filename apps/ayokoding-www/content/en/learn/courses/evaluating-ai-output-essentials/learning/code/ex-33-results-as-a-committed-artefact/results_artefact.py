# learning/code/ex-33-results-as-a-committed-artefact/results_artefact.py
"""Worked Example 33: Results as a Committed Artefact."""  # => co-07: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import json  # => co-07: the artefact format needs nothing beyond the standard library's own json module
from pathlib import Path  # => co-07: locates results.json relative to this script, not the caller's cwd

RESULTS_PATH = Path(__file__).parent / "results.json"  # => co-09: the committed artefact THIS run produces
FIXED_RESULTS: dict[str, object] = {  # => co-07: a small, fixed run's worth of results -- deterministic, not sampled
    "run_id": "prompt-v1-baseline",  # => co-09: names WHICH version of the system produced this artefact
    "pass_rate": 0.9167,  # => co-07: the headline number from ex-23's run
    "cases": {"case-01": "PASS", "case-11": "FAIL"},  # => co-07: a trimmed per-case snapshot for this example
}  # => co-07: closes FIXED_RESULTS


def write_results(path: Path, results: dict[str, object]) -> None:  # => co-09: persist the run's results to disk
    """Write `results` to `path` as pretty-printed, deterministically-ordered JSON."""  # => co-09: documents write_results's contract -- no runtime output, just sets its __doc__
    path.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")  # => co-09: sort_keys -- same input, same bytes, every time


if __name__ == "__main__":  # => co-07: entry point -- runs only when this file executes directly, not on import
    write_results(RESULTS_PATH, FIXED_RESULTS)  # => co-09: "run 1" -- writes the artefact to disk
    first_write = RESULTS_PATH.read_text(encoding="utf-8")  # => co-09: read back exactly what run 1 wrote
    write_results(RESULTS_PATH, FIXED_RESULTS)  # => co-09: "run 2" -- writes the SAME artefact again
    second_write = RESULTS_PATH.read_text(encoding="utf-8")  # => co-09: read back exactly what run 2 wrote
    print(first_write)  # => co-09: prints the committed artefact's exact contents
    reproducible = first_write == second_write  # => co-09: byte-for-byte identical, not just "similar"
    print(f"Byte-identical across two writes: {reproducible}")  # => co-09: prints the reproducibility check
    assert reproducible, "the same results must serialize to byte-identical JSON on every write"  # => co-09
    print("MATCH: results.json is a reproducible artefact another engineer can open and re-check by hand")  # => co-07
    # => co-09: a comparison (ex-37) is only trustworthy if the baseline it compares against is itself a stable, committed file
