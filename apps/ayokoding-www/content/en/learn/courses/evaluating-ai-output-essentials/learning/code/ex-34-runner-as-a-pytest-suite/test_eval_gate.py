# learning/code/ex-34-runner-as-a-pytest-suite/test_eval_gate.py
"""Worked Example 34: Runner as a Pytest Suite."""  # => co-05: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import json  # => co-03: JSONL needs nothing beyond the standard library's own json module
import re  # => co-05: backs the regex and numeric_tolerance scorer entries below
from pathlib import Path  # => co-03: locates dataset.jsonl relative to this file, not pytest's own cwd

import pytest  # => co-05: no separate eval framework -- ordinary pytest IS the runner

DATASET_PATH = Path(__file__).parent / "dataset.jsonl"  # => co-03: the same twelve-case fixed gate as ex-23
NUMBER_PATTERN = re.compile(r"-?\d+(?:\.\d+)?")  # => co-05: shared by the numeric_tolerance scorer below
SYSTEM_ANSWERS = {  # => co-01: the same mocked "prompt v1" answers as ex-23, unchanged
    "case-01": "New Nimbus accounts start with 15 GB of free storage.",  # => co-01: correct
    "case-02": "Nimbus Pro includes 200 GB of storage.",  # => co-01: correct
    "case-03": "Yes, Nimbus supports two-factor authentication.",  # => co-01: correct
    "case-04": "The Nimbus app shipped on iOS first.",  # => co-01: correct
    "case-05": "The Free plan accepts files up to 5 GB in size.",  # => co-01: correct
    "case-06": "The Pro plan accepts files up to 50 GB in size.",  # => co-01: correct
    "case-07": "Share links expire automatically after 30 days.",  # => co-01: correct
    "case-08": "Free-plan email support targets a 24-hour first response.",  # => co-01: correct
    "case-09": "Deleted files stay in trash for 30 days.",  # => co-01: correct
    "case-10": "pro only",  # => co-01: correct, short classification-style output
    "case-11": "The public REST API is available on the Free plan too.",  # => co-01: WRONG -- it's Pro-only
    "case-12": "Files are encrypted at rest using AES-256.",  # => co-01: correct
}  # => co-01: closes SYSTEM_ANSWERS -- eleven correct, one deliberately wrong


def score(scorer_name: str, output: str, expected: str) -> bool:  # => co-05: the same four-entry registry as ex-23
    if scorer_name == "exact_match":  # => co-05: dispatch branch 1
        return output.strip().lower() == expected.strip().lower()  # => co-05: normalized equality
    if scorer_name == "substring":  # => co-05: dispatch branch 2
        return expected in output  # => co-05: the fact just has to appear somewhere
    if scorer_name == "regex":  # => co-05: dispatch branch 3
        return re.search(expected, output) is not None  # => co-05: expected doubles as the pattern text
    match = NUMBER_PATTERN.search(output)  # => co-05: dispatch branch 4 (numeric_tolerance)
    return match is not None and abs(float(match.group()) - float(expected)) <= 1.0  # => co-05: within +-1 tolerance


def _load_cases() -> list[dict[str, str]]:  # => co-03: loads the dataset ONCE, at collection time
    """Load the committed dataset.jsonl for use as pytest.mark.parametrize's own case list."""  # => co-03: documents _load_cases's contract -- no runtime output, just sets its __doc__
    return [json.loads(line) for line in DATASET_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]  # => co-03


@pytest.mark.parametrize("case", _load_cases(), ids=lambda c: c["id"])  # => co-07: ONE test function, TWELVE reported test results
def test_case_passes_its_own_scorer(case: dict[str, str]) -> None:  # => co-07: this IS the eval, expressed as a pytest test
    """Each dataset case must pass the scorer it declares for itself."""  # => co-07: documents test_case_passes_its_own_scorer's contract -- no runtime output, just sets its __doc__
    output = SYSTEM_ANSWERS[case["id"]]  # => co-01: "call the system" -- mocked, offline, no API key
    verdict = score(case["scorer"], output, case["expected"])  # => co-05: apply this case's own declared scorer
    assert verdict, f"{case['id']} failed its {case['scorer']} scorer"  # => co-07: pytest's own assert IS the pass/fail gate
