# learning/code/ex-36-candidate-run/candidate_run.py
"""Worked Example 36: Candidate Run."""  # => co-09: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import json  # => co-09: the artefact format needs nothing beyond the standard library's own json module
from pathlib import Path  # => co-09: locates candidate.json relative to this script, not the caller's cwd

CANDIDATE_PATH = Path(__file__).parent / "candidate.json"  # => co-09: the committed artefact THIS run produces
PROMPT_V2_VERDICTS = {  # => co-09: "prompt v2" -- a proposed rewrite, run against the SAME twelve cases as ex-35
    "case-01": True,  # => co-09: pass
    "case-02": True,  # => co-09: pass
    "case-03": True,  # => co-09: pass
    "case-04": True,  # => co-09: cases 1-4 -- unchanged, still pass
    "case-05": True,  # => co-09: pass
    "case-06": True,  # => co-09: now fixed
    "case-07": True,  # => co-09: pass
    "case-08": True,  # => co-09: case 6 and 8 -- NOW FIXED
    "case-09": True,  # => co-09: pass
    "case-10": True,  # => co-09: pass
    "case-11": True,  # => co-09: now fixed
    "case-12": True,  # => co-09: case 11 -- NOW FIXED
}  # => co-09: closes PROMPT_V2_VERDICTS -- all twelve pass


if __name__ == "__main__":  # => co-09: entry point -- runs only when this file executes directly, not on import
    pass_rate = sum(PROMPT_V2_VERDICTS.values()) / len(PROMPT_V2_VERDICTS)  # => co-07: the candidate's headline number
    candidate = {"run_id": "prompt-v2", "pass_rate": pass_rate, "verdicts": PROMPT_V2_VERDICTS}  # => co-09: the full candidate artefact
    CANDIDATE_PATH.write_text(json.dumps(candidate, indent=2, sort_keys=True) + "\n", encoding="utf-8")  # => co-09: commit it to disk
    print(f"Candidate pass rate: {pass_rate:.2%}")  # => co-07: prints the stored headline number
    print(f"Written to {CANDIDATE_PATH.name}")  # => co-09: prints where the artefact landed
    assert pass_rate == 1.0, "the candidate's fixed verdicts must reduce to exactly 100%"  # => co-07: confirms the arithmetic
    assert set(PROMPT_V2_VERDICTS) == {f"case-{n:02d}" for n in range(1, 13)}, "the candidate must cover the SAME case set"  # => co-09
    print("MATCH: the candidate ran against the identical case set the baseline used -- a genuinely comparable number")  # => co-09
    # => co-09: a comparable number requires the SAME fixed dataset -- swap the dataset and you've measured something else
