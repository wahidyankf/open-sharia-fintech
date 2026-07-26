# learning/code/ex-16-schema-validation-scorer/schema_scorer.py
"""Worked Example 16: Schema-Validation Scorer."""  # => co-06: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

REQUIRED_SCHEMA = {"answer": str, "confidence": float, "source_fact_id": str}  # => co-06: the structured-output contract


def schema_scorer(output: dict[str, object], schema: dict[str, type]) -> tuple[bool, str]:  # => co-06: structure, not content
    """Pass iff every schema key is present in `output` AND has the schema's declared type."""  # => co-06: documents schema_scorer's contract -- no runtime output, just sets its __doc__
    for key, expected_type in schema.items():  # => co-06: check each required field independently
        if key not in output:  # => co-06: the cheapest possible failure -- a field is simply absent
            return False, f"missing field: {key}"  # => co-06: a reason naming the exact missing field
        if not isinstance(output[key], expected_type):  # => co-06: present, but the WRONG type
            actual_type = type(output[key]).__name__  # => co-06: what type actually showed up
            return False, f"field {key} has type {actual_type}, expected {expected_type.__name__}"  # => co-06
    return True, "all fields present with correct types"  # => co-06: every check passed


if __name__ == "__main__":  # => co-06: entry point -- runs only when this file executes directly, not on import
    well_formed: dict[str, object] = {"answer": "15 GB", "confidence": 0.92, "source_fact_id": "storage-free"}  # => co-06: satisfies the schema
    missing_field: dict[str, object] = {"answer": "15 GB", "confidence": 0.92}  # => co-06: source_fact_id is simply absent
    wrong_type: dict[str, object] = {"answer": "15 GB", "confidence": "high", "source_fact_id": "storage-free"}  # => co-06: confidence is a str, not a float
    well_formed_result = schema_scorer(well_formed, REQUIRED_SCHEMA)  # => co-06: the pass path
    missing_result = schema_scorer(missing_field, REQUIRED_SCHEMA)  # => co-06: the missing-field fail path
    wrong_type_result = schema_scorer(wrong_type, REQUIRED_SCHEMA)  # => co-06: the wrong-type fail path
    print(f"well_formed -> {well_formed_result}")  # => co-06: prints the pass verdict + reason
    print(f"missing_field -> {missing_result}")  # => co-06: prints the missing-field verdict + reason
    print(f"wrong_type -> {wrong_type_result}")  # => co-06: prints the wrong-type verdict + reason
    assert well_formed_result[0] is True, "a fully schema-conformant output must pass"  # => co-06: confirms the pass path
    assert missing_result == (False, "missing field: source_fact_id"), "a missing field must fail with that exact reason"  # => co-06
    assert wrong_type_result[0] is False, "a wrong-typed field must fail validation"  # => co-06: confirms the type check fires
    print("MATCH: schema validation is the cheapest, highest-value eval for any structured-output feature")  # => co-06
    # => co-06: schema validation runs in microseconds and needs no model call of its own -- pure structural verification
