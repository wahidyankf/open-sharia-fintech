# learning/code/ex-35-baseline-run/baseline_run.py
"""Worked Example 35: Baseline Run."""  # => co-09: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import json  # => co-09: the artefact format needs nothing beyond the standard library's own json module
from pathlib import Path  # => co-09: locates baseline.json relative to this script, not the caller's cwd

BASELINE_PATH = Path(__file__).parent / "baseline.json"  # => co-09: the committed artefact THIS run produces
PROMPT_V1_VERDICTS = {  # => co-01: "prompt v1" -- the version currently shipped, before any change is proposed
    "case-01": True,  # => co-01: pass
    "case-02": True,  # => co-01: pass
    "case-03": True,  # => co-01: pass
    "case-04": True,  # => co-01: cases 1-4 -- all pass
    "case-05": True,  # => co-01: pass
    "case-06": False,  # => co-01: known failure
    "case-07": True,  # => co-01: pass
    "case-08": False,  # => co-01: case 6 and 8 -- known failures
    "case-09": True,  # => co-01: pass
    "case-10": True,  # => co-01: pass
    "case-11": False,  # => co-01: known failure
    "case-12": True,  # => co-01: case 11 -- a third known failure
}  # => co-01: closes PROMPT_V1_VERDICTS -- nine pass, three fail


if __name__ == "__main__":  # => co-09: entry point -- runs only when this file executes directly, not on import
    pass_rate = sum(PROMPT_V1_VERDICTS.values()) / len(PROMPT_V1_VERDICTS)  # => co-07: the baseline's headline number
    baseline = {"run_id": "prompt-v1", "pass_rate": pass_rate, "verdicts": PROMPT_V1_VERDICTS}  # => co-09: the full baseline artefact
    BASELINE_PATH.write_text(json.dumps(baseline, indent=2, sort_keys=True) + "\n", encoding="utf-8")  # => co-09: commit it to disk
    print(f"Baseline pass rate: {pass_rate:.2%}")  # => co-07: prints the stored headline number
    print(f"Written to {BASELINE_PATH.name}")  # => co-09: prints where the artefact landed
    assert pass_rate == 0.75, "the baseline's fixed verdicts must reduce to exactly 75%"  # => co-07: confirms the arithmetic
    print("MATCH: the baseline is measured and stored BEFORE any prompt change is proposed")  # => co-09
    # => co-09: without a stored baseline, ex-37's comparison would have nothing to compare the candidate against
