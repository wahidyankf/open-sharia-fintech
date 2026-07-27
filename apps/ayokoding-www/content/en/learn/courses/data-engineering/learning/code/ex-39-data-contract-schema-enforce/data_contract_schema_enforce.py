"""Worked Example 39: Data Contract -- Enforce a Producer Schema."""  # => co-17: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

CONTRACT = {  # => co-17: the PRODUCER's own enforceable promise -- columns, types, and not-null, checked BEFORE the build proceeds
    "order_id": {"type": int, "nullable": False},  # => co-17: required column 1 -- INTEGER, never null
    "amount": {"type": float, "nullable": False},  # => co-17: required column 2 -- FLOAT, never null
    "status": {"type": str, "nullable": True},  # => co-17: required column 3 -- STRING, nulls allowed
}  # => co-17: closes CONTRACT -- dbt's own "model contracts" enforce exactly this shape, failing the build on drift


def enforce_contract(batch: list[dict[str, object]], contract: dict[str, dict[str, object]]) -> tuple[bool, str]:  # => co-17: the enforcement itself
    """Fail the build (return False) the moment any row violates the contract's columns, types, or nullability."""  # => co-17: documents enforce_contract's contract -- no runtime output, just sets its __doc__
    for row_index, row in enumerate(batch):  # => co-17: check every row -- one violation anywhere fails the WHOLE build
        for column, rule in contract.items():  # => co-17: check every contracted column against this row
            if column not in row:  # => co-17: SCHEMA DRIFT -- a contracted column is entirely missing from this row
                return False, f"row {row_index}: missing contracted column {column!r}"  # => co-17: fail closed, name the exact drift
            value = row[column]  # => co-17: this row's value for the contracted column
            if value is None:  # => co-17: a null value -- only acceptable if the contract explicitly allows it
                if not rule["nullable"]:  # => co-17: this column's contract forbids null
                    return False, f"row {row_index}: {column!r} is null but the contract forbids that"  # => co-17: fail closed
                continue  # => co-17: null, but ALLOWED by contract -- move on to the next column
            if not isinstance(value, rule["type"]):  # => co-17: WRONG TYPE -- present, but not the contracted type
                return False, f"row {row_index}: {column!r} has type {type(value).__name__}, contract requires {rule['type'].__name__}"  # => co-17
    return True, "every row satisfies the contract"  # => co-17: reached only if EVERY row, EVERY column, passed


if __name__ == "__main__":  # => co-17: entry point -- runs only when this file executes directly, not on import
    conforming_batch = [{"order_id": 1, "amount": 10.5, "status": "shipped"}, {"order_id": 2, "amount": 20.0, "status": None}]  # => co-17: satisfies CONTRACT
    drifted_batch = [{"order_id": 1, "amount": "not-a-number", "status": "shipped"}]  # => co-17: amount is a STRING, not a float -- schema drift

    conforming_passed, conforming_reason = enforce_contract(conforming_batch, CONTRACT)  # => co-17: check the conforming batch
    drifted_passed, drifted_reason = enforce_contract(drifted_batch, CONTRACT)  # => co-17: check the drifted batch
    print(f"Conforming batch: passed={conforming_passed} ({conforming_reason})")  # => co-17: prints the conforming result
    print(f"Drifted batch: passed={drifted_passed} ({drifted_reason})")  # => co-17: prints the drifted result, with the exact reason

    assert conforming_passed is True, "a batch matching every contracted column/type/nullability rule must pass"  # => co-17: the claim
    assert drifted_passed is False, "a schema-drifting batch (wrong type) must fail the build, not silently proceed"  # => co-17: the claim
    print("MATCH: the conforming batch passes; the type-drifted batch fails the build BEFORE it reaches downstream tables")  # => co-17
    # => co-17: a data contract fails the BUILD on drift -- the alternative (silent drift) corrupts every downstream consumer instead
