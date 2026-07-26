# learning/code/ex-19-scorer-registry/scorer_registry.py
"""Worked Example 19: Scorer Registry."""  # => co-05: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import json  # => co-03: JSONL needs nothing beyond the standard library's own json module
import re  # => co-05: the regex-scorer entry needs the standard library's own re module
from pathlib import Path  # => co-03: locates dataset.jsonl relative to this script, not the caller's cwd
from typing import Callable  # => co-05: types the registry's values as callables, not just "some function"

DATASET_PATH = Path(__file__).parent / "dataset.jsonl"  # => co-03: the twelve-case dataset, each case naming its own scorer
NUMBER_PATTERN = re.compile(r"-?\d+(?:\.\d+)?")  # => co-05: shared by the numeric_tolerance entry below


def exact_match(output: str, expected: str) -> bool:  # => co-05: registry entry "exact_match"
    return output.strip().lower() == expected.strip().lower()  # => co-05: normalized, matching ex-12's fix


def substring(output: str, expected: str) -> bool:  # => co-05: registry entry "substring"
    return expected in output  # => co-05: the fact just has to appear somewhere


def regex(output: str, expected: str) -> bool:  # => co-05: registry entry "regex" -- `expected` doubles as the pattern text
    return re.search(expected, output) is not None  # => co-05: search for the pattern text anywhere in the output


def numeric_tolerance(output: str, expected: str) -> bool:  # => co-05: registry entry "numeric_tolerance"
    match = NUMBER_PATTERN.search(output)  # => co-05: locate the first number in the free-text answer
    return match is not None and abs(float(match.group()) - float(expected)) <= 1.0  # => co-05: within a fixed +-1 tolerance


SCORER_REGISTRY: dict[str, Callable[[str, str], bool]] = {  # => co-05: name -> function, ONE lookup table for every case
    "exact_match": exact_match,  # => co-05: maps the dataset's "exact_match" string to this function
    "substring": substring,  # => co-05: maps the dataset's "substring" string to this function
    "regex": regex,  # => co-05: maps the dataset's "regex" string to this function
    "numeric_tolerance": numeric_tolerance,  # => co-05: maps the dataset's "numeric_tolerance" string to this function
}  # => co-05: closes the registry dict


if __name__ == "__main__":  # => co-05: entry point -- runs only when this file executes directly, not on import
    cases = [json.loads(line) for line in DATASET_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]  # => co-03
    print(f"Dispatching {len(cases)} cases through the scorer registry")  # => co-05: states the sample size up front
    dispatched_names: set[str] = set()  # => co-05: which registry entries actually got exercised
    for case in cases:  # => co-05: one dispatch per case, driven entirely by data, not an if/elif chain
        scorer_fn = SCORER_REGISTRY[case["scorer"]]  # => co-05: the case's own "scorer" field picks the function, by name
        dispatched_names.add(case["scorer"])  # => co-05: records that this scorer name was actually reached
        verdict = scorer_fn(case["expected"], case["expected"])  # => co-05: a trivial self-check -- the fact scores against itself
        assert verdict is True, f"{case['id']}'s own expected value must score True against itself"  # => co-05: a sanity fixture
    print(f"Registry entries exercised: {sorted(dispatched_names)}")  # => co-05: prints exactly which scorer names got used
    assert dispatched_names == set(SCORER_REGISTRY), "every registered scorer must be reachable from real dataset cases"  # => co-05
    print("MATCH: every case reached the correct scorer purely by its own 'scorer' field -- no manual routing")  # => co-05
    # => co-05: a registry keeps the runner (ex-23) ignorant of which scorer any given case needs -- the data decides
