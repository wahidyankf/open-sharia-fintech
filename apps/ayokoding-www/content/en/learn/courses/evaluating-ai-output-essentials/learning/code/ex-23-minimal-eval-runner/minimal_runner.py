# learning/code/ex-23-minimal-eval-runner/minimal_runner.py
"""Worked Example 23: Minimal Eval Runner."""  # => co-07: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import json  # => co-03: JSONL needs nothing beyond the standard library's own json module
import re  # => co-05: backs the regex and numeric_tolerance scorer entries below
from pathlib import Path  # => co-03: locates dataset.jsonl relative to this script, not the caller's cwd

DATASET_PATH = Path(__file__).parent / "dataset.jsonl"  # => co-03: the twelve-case fixed gate this runner exercises
NUMBER_PATTERN = re.compile(r"-?\d+(?:\.\d+)?")  # => co-05: shared by the numeric_tolerance scorer below

SYSTEM_ANSWERS = {  # => co-01: "prompt v1" -- the mocked system-under-test's canned answer for each case id
    "case-01": "New Nimbus accounts start with 15 GB of free storage.",  # => co-01: correct
    "case-02": "Nimbus Pro includes 200 GB of storage.",  # => co-01: correct
    "case-03": "Yes, Nimbus supports two-factor authentication for account security.",  # => co-01: correct
    "case-04": "The Nimbus app shipped on iOS first.",  # => co-01: correct
    "case-05": "The Free plan accepts files up to 5 GB in size.",  # => co-01: correct
    "case-06": "The Pro plan accepts files up to 50 GB in size.",  # => co-01: correct
    "case-07": "Share links expire automatically after 30 days.",  # => co-01: correct
    "case-08": "Free-plan email support targets a 24-hour first response.",  # => co-01: correct
    "case-09": "Deleted files stay in trash for 30 days before permanent deletion.",  # => co-01: correct
    "case-10": "pro only",  # => co-01: correct, short classification-style output
    "case-11": "The public REST API is available on the Free plan too.",  # => co-01: WRONG -- it's Pro-only
    "case-12": "Files are encrypted at rest using AES-256.",  # => co-01: correct
}  # => co-01: closes SYSTEM_ANSWERS -- eleven correct, one deliberately wrong


def score(scorer_name: str, output: str, expected: str) -> bool:  # => co-05: the same four-entry registry idea from ex-19
    if scorer_name == "exact_match":  # => co-05: dispatch branch 1
        return output.strip().lower() == expected.strip().lower()  # => co-05: normalized equality
    if scorer_name == "substring":  # => co-05: dispatch branch 2
        return expected in output  # => co-05: the fact just has to appear somewhere
    if scorer_name == "regex":  # => co-05: dispatch branch 3
        return re.search(expected, output) is not None  # => co-05: expected doubles as the pattern text
    match = NUMBER_PATTERN.search(output)  # => co-05: dispatch branch 4 (numeric_tolerance) -- find the first number
    return match is not None and abs(float(match.group()) - float(expected)) <= 1.0  # => co-05: within +-1 tolerance


if __name__ == "__main__":  # => co-07: entry point -- runs only when this file executes directly, not on import
    cases = [json.loads(line) for line in DATASET_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]  # => co-03
    results: list[bool] = []  # => co-07: one verdict per case, in dataset order
    for case in cases:  # => co-07: the whole runner, in five lines -- load, call, score, record, report
        output = SYSTEM_ANSWERS[case["id"]]  # => co-01: "call the system" -- mocked, offline, no API key
        verdict = score(case["scorer"], output, case["expected"])  # => co-05: apply the case's own declared scorer
        results.append(verdict)  # => co-07: record this case's pass/fail
        print(f"{case['id']}: {'PASS' if verdict else 'FAIL'}")  # => co-07: one printed line per case, end to end
    pass_rate = sum(results) / len(results)  # => co-07: the single headline number -- fraction of cases passing
    print(f"Pass rate: {pass_rate:.2%} ({sum(results)}/{len(results)})")  # => co-07: prints the headline number
    assert len(results) == 12, "the runner must produce one verdict per dataset case"  # => co-07: sanity check
    assert sum(results) == 11, "exactly eleven of twelve cases must pass against this fixed dataset"  # => co-07
    print("MATCH: dataset loaded, system called, scorer applied, pass rate reported -- end to end")  # => co-07
    # => co-07: this IS the eval gate -- everything from here is refining pass rate, repeat runs, and comparison
