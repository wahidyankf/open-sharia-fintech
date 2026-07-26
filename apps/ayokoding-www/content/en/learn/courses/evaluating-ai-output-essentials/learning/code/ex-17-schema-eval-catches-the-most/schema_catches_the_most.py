# learning/code/ex-17-schema-eval-catches-the-most/schema_catches_the_most.py
"""Worked Example 17: Schema Eval Catches the Most."""  # => co-06: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

REQUIRED_SCHEMA = {"answer": str, "confidence": float, "source_fact_id": str}  # => co-06: the same structured-output contract as ex-16

BROKEN_OUTPUTS: list[dict[str, object]] = [  # => co-06: five outputs, each broken in a DIFFERENT realistic way
    {"answer": "15 GB", "source_fact_id": "storage-free"},  # => co-06: defect 1 -- confidence field simply missing
    {"answer": "15 GB", "confidence": "high", "source_fact_id": "storage-free"},  # => co-06: defect 2 -- confidence wrong type
    {"answer": "15 GB", "confidence": 0.9},  # => co-06: defect 3 -- source_fact_id field simply missing
    {"answer": 15, "confidence": 0.9, "source_fact_id": "storage-free"},  # => co-06: defect 4 -- answer wrong type (int, not str)
    {"answer": "15 GB", "confidence": 0.9, "source_fact_id": None},  # => co-06: defect 5 -- source_fact_id wrong type (None)
]  # => co-06: closes the broken-outputs list


def schema_scorer(output: dict[str, object], schema: dict[str, type]) -> bool:  # => co-06: structural check -- every field, every type
    """Pass iff every schema key is present in `output` with the schema's declared type."""  # => co-06: documents schema_scorer's contract -- no runtime output, just sets its __doc__
    return all(key in output and isinstance(output[key], expected) for key, expected in schema.items())  # => co-06: one line, all fields


def substring_sanity_check(output: dict[str, object]) -> bool:  # => co-06: a cheaper-LOOKING check that only inspects "answer"
    """Pass iff the (string-coerced) 'answer' field contains a plausible-looking fact -- ignores every other field."""  # => co-06: documents substring_sanity_check's contract -- no runtime output, just sets its __doc__
    return "GB" in str(output.get("answer", ""))  # => co-06: never looks at confidence or source_fact_id at all


if __name__ == "__main__":  # => co-06: entry point -- runs only when this file executes directly, not on import
    schema_catches = sum(not schema_scorer(o, REQUIRED_SCHEMA) for o in BROKEN_OUTPUTS)  # => co-06: how many of the five it flags
    substring_catches = sum(not substring_sanity_check(o) for o in BROKEN_OUTPUTS)  # => co-06: how many the shallow check flags
    print(f"Broken outputs: {len(BROKEN_OUTPUTS)}")  # => co-06: states the sample size up front
    print(f"schema_scorer catches: {schema_catches}/{len(BROKEN_OUTPUTS)}")  # => co-06: the structural scorer's catch rate
    print(f"substring_sanity_check catches: {substring_catches}/{len(BROKEN_OUTPUTS)}")  # => co-06: the shallow scorer's catch rate
    assert schema_catches == 5, "schema_scorer must catch all five structural defects"  # => co-06: verifies the claim, not just asserts it
    assert substring_catches == 1, "substring_sanity_check must catch only the one defect that happens to touch 'answer'"  # => co-06
    print("MATCH: one schema check catches 5x more real breakage than a shallow field-only check, for one line of code")  # => co-06
    # => co-06: this is exactly why co-06 ranks schema validation as the highest-value eval per line of eval code written
