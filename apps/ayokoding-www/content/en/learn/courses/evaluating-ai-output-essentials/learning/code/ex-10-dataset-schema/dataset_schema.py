# learning/code/ex-10-dataset-schema/dataset_schema.py
"""Worked Example 10: Dataset Schema."""  # => co-03: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import json  # => co-03: JSONL needs nothing beyond the standard library's own json module
from pathlib import Path  # => co-03: locates dataset.jsonl relative to this script, not the caller's cwd

DATASET_PATH = Path(__file__).parent / "dataset.jsonl"  # => co-03: the twelve-case dataset ex-05 committed
REQUIRED_KEYS = {"id", "input", "expected", "criterion"}  # => co-04: co-10's spec -- the minimal case schema, exactly four keys
MALFORMED_CASE: dict[str, object] = {"id": "case-99", "input": "How much does Nimbus Pro cost?"}  # => co-04: a case someone forgot to finish


def validate_case(case: dict[str, object]) -> tuple[bool, str]:  # => co-04: one case in, one pass/fail-plus-reason out
    """Pass iff every REQUIRED_KEYS entry is present in `case`; the reason names exactly what's missing."""  # => co-04: documents validate_case's contract -- no runtime output, just sets its __doc__
    present_keys = set(case.keys())  # => co-04: what this case actually declares
    missing_keys = REQUIRED_KEYS - present_keys  # => co-04: what the schema demands but this case omits
    passed = len(missing_keys) == 0  # => co-04: valid iff nothing required is missing
    reason = "all required keys present" if passed else f"missing keys: {sorted(missing_keys)}"  # => co-04: a reason anyone can re-check
    return passed, reason  # => co-04: returns this computed value to the caller


if __name__ == "__main__":  # => co-04: entry point -- runs only when this file executes directly, not on import
    raw_lines = DATASET_PATH.read_text(encoding="utf-8").splitlines()  # => co-04: the committed dataset, one line per case
    cases = [json.loads(line) for line in raw_lines if line.strip()]  # => co-04: parse every non-blank line
    print(f"Validating {len(cases)} committed cases against {sorted(REQUIRED_KEYS)}")  # => co-04: states the schema up front
    results = [validate_case(case) for case in cases]  # => co-04: one (passed, reason) pair per committed case
    all_valid = all(passed for passed, _ in results)  # => co-04: the whole dataset's schema verdict
    print(f"Every committed case validates: {all_valid}")  # => co-04: True -- every case satisfies the schema
    assert all_valid, "every committed case must satisfy the minimal schema"  # => co-04: the claim ex-10 makes

    malformed_passed, malformed_reason = validate_case(MALFORMED_CASE)  # => co-04: the schema applied to an UNFINISHED case
    print(f"Malformed case validates: {malformed_passed} ({malformed_reason})")  # => co-04: False, with a precise reason
    assert not malformed_passed, "a case missing required keys must fail validation"  # => co-04: rejection, not a silent pass
    assert malformed_reason == "missing keys: ['criterion', 'expected']", "the reason must name exactly what's missing"  # => co-04
    print("MATCH: schema validation both accepts every finished case and rejects the unfinished one")  # => co-04
    # => co-04: a case schema is what turns "I collected some inputs" into "every case is a real, checkable eval unit"
