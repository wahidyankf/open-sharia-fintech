# learning/capstone/code/scorers.py
"""Capstone step 2: the five-scorer registry, plus one loose scorer and its fix (exercises co-05, co-06, co-02)."""  # => co-05: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import re  # => co-05: backs the regex and numeric_tolerance scorers
from typing import Callable, NamedTuple, cast  # => co-05: types the registry's values; Verdict is a typed record; cast narrows a bare-dict isinstance check

NUMBER_PATTERN = re.compile(r"-?\d+(?:\.\d+)?")  # => co-05: shared by numeric_tolerance -- finds the first number in free text
STRUCTURED_SCHEMA = {"status": str, "storage_used_gb": float, "plan": str}  # => co-06: case-14's required structure


class Verdict(NamedTuple):  # => co-05: EVERY scorer in this capstone returns this shape
    passed: bool  # => co-05: the pass/fail decision
    reason: str  # => co-05: WHY -- readable without re-deriving it from the raw output


def exact_match(output: object, expected: str) -> Verdict:  # => co-05: registry entry "exact_match"
    """Pass iff `output` equals `expected` exactly, character for character."""  # => co-05: documents exact_match's contract -- no runtime output, just sets its __doc__
    passed = str(output) == expected  # => co-05: no normalization at all -- byte-identical or fail
    return Verdict(passed, "exact match" if passed else f"expected exactly {expected!r}, got {output!r}")  # => co-05


def normalized_match(output: object, expected: str) -> Verdict:  # => co-05: registry entry "normalized_match"
    """Pass iff `output` equals `expected` after lowercasing and stripping whitespace."""  # => co-05: documents normalized_match's contract -- no runtime output, just sets its __doc__
    normalized_output = str(output).strip().lower()  # => co-05: removes purely cosmetic differences
    passed = normalized_output == expected.strip().lower()  # => co-05: both sides normalized identically
    return Verdict(passed, "normalized match" if passed else f"expected {expected!r} after normalizing, got {output!r}")  # => co-05


def regex(output: object, expected: str) -> Verdict:  # => co-05: registry entry "regex" -- expected doubles as the pattern text
    """Pass iff `expected` (used as a pattern) is found anywhere inside `output`."""  # => co-05: documents regex's contract -- no runtime output, just sets its __doc__
    passed = re.search(expected, str(output)) is not None  # => co-05: search, not match -- the pattern may sit anywhere
    return Verdict(passed, f"pattern {expected!r} found" if passed else f"pattern {expected!r} not found in {output!r}")  # => co-05


def numeric_tolerance(output: object, expected: str, *, tolerance: float = 1.0) -> Verdict:  # => co-05: registry entry
    """Pass iff the first number in `output` is within `tolerance` of `float(expected)`."""  # => co-05: documents numeric_tolerance's contract -- no runtime output, just sets its __doc__
    match = NUMBER_PATTERN.search(str(output))  # => co-05: locate the first numeric token
    if match is None:  # => co-05: no number at all -- cannot satisfy a numeric criterion
        return Verdict(False, f"no number found in {output!r}")  # => co-05: fail closed rather than raising
    found = float(match.group())  # => co-05: parse the matched substring into an actual float
    passed = abs(found - float(expected)) <= tolerance  # => co-05: within tolerance, inclusive of the boundary
    return Verdict(passed, f"{found} within {tolerance} of {expected}" if passed else f"{found} not within {tolerance} of {expected}")  # => co-05


def schema(output: object, expected: str) -> Verdict:  # => co-06: registry entry "schema" -- structure, not content
    """Pass iff `output` is a dict with every STRUCTURED_SCHEMA key present, correctly typed."""  # => co-06: documents schema's contract -- no runtime output, just sets its __doc__
    del expected  # => co-06: unused -- the schema itself is the fixed contract, not per-case data
    if not isinstance(output, dict):  # => co-06: the cheapest possible rejection -- not even a mapping
        return Verdict(False, f"expected a dict, got {type(output).__name__}")  # => co-06
    output_map = cast(dict[str, object], output)  # => co-06: bare-dict narrowing gives dict[Unknown, Unknown] -- cast restores a checkable value type
    for key, expected_type in STRUCTURED_SCHEMA.items():  # => co-06: check each required field independently
        if key not in output_map:  # => co-06: a field is simply absent
            return Verdict(False, f"missing field: {key}")  # => co-06: a reason naming the exact missing field
        if not isinstance(output_map[key], expected_type):  # => co-06: present, but the WRONG type
            return Verdict(False, f"field {key} has type {type(output_map[key]).__name__}, expected {expected_type.__name__}")  # => co-06
    return Verdict(True, "all fields present with correct types")  # => co-06: every check passed


def loose_fact_scorer(output: object, expected: str) -> Verdict:  # => co-02: DELIBERATELY over-permissive -- ex-20's lesson
    """An over-permissive scorer -- passes if the output merely contains ANY digit at all."""  # => co-02: documents loose_fact_scorer's contract -- no runtime output, just sets its __doc__
    del expected  # => co-02: unused -- that IS the bug, this scorer ignores the specific expected value
    passed = any(char.isdigit() for char in str(output))  # => co-02: satisfied by ANY number, right or wrong
    return Verdict(passed, "contains a digit" if passed else "contains no digit at all")  # => co-02


SCORER_REGISTRY: dict[str, Callable[..., Verdict]] = {  # => co-05: name -> function, ONE lookup table for every case
    "exact_match": exact_match,  # => co-05: entry 1
    "normalized_match": normalized_match,  # => co-05: entry 2
    "regex": regex,  # => co-05: entries 1-3
    "numeric_tolerance": numeric_tolerance,  # => co-05: entry 4
    "schema": schema,  # => co-05: entries 4-5
}  # => co-05: closes SCORER_REGISTRY -- exactly the five scorer types this capstone step builds


if __name__ == "__main__":  # => co-05: entry point -- runs only when this file executes directly, not on import
    loose_verdict = loose_fact_scorer("Nimbus Pro includes 20 GB.", "200 GB")  # => co-02: the wrong figure, scored by the loose scorer
    tight_verdict = regex("Nimbus Pro includes 20 GB.", "200 GB")  # => co-02: the SAME wrong output, scored by the tightened regex scorer
    print(f"Loose scorer on a WRONG answer: {loose_verdict}")  # => co-02: prints the false pass
    print(f"Tightened scorer on the SAME wrong answer: {tight_verdict}")  # => co-02: prints the corrected fail
    assert loose_verdict.passed is True, "the loose scorer must wrongly pass a factually wrong answer"  # => co-02: proves the lie
    assert tight_verdict.passed is False, "the tightened regex scorer must catch the same wrong answer"  # => co-02: confirms the fix
    for name, fn in SCORER_REGISTRY.items():  # => co-05: a quick self-check that every registered scorer is callable
        assert callable(fn), f"registry entry {name!r} must be callable"  # => co-05: sanity check
    print(f"MATCH: {len(SCORER_REGISTRY)} deterministic scorers registered, each returning (passed, reason)")  # => co-05
    # => co-05: runner.py imports SCORER_REGISTRY directly -- no case ever routes through the loose scorer above
