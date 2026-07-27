"""Worked Example 40: Contract Close to the Producer."""  # => co-17: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

CALL_LOG: list[str] = []  # => co-17: records the ORDER in which produce, contract-check, and downstream-read actually run


def produce_row() -> dict[str, object]:  # => co-17: the MODEL that produces this row -- the contract must sit right here, not downstream
    """Produce one row -- a deliberately drifted one, missing its required 'amount' column."""  # => co-17: documents produce_row's contract -- no runtime output, just sets its __doc__
    CALL_LOG.append("produce")  # => co-17: log this stage's participation
    return {"order_id": 99}  # => co-17: DRIFTED -- missing the contracted 'amount' column entirely


def check_contract_at_produce_time(row: dict[str, object]) -> bool:  # => co-17: co-located WITH the producing model, run IMMEDIATELY after produce
    """Check the contract immediately after production, before this row can reach any downstream reader."""  # => co-17: documents check_contract_at_produce_time's contract -- no runtime output, just sets its __doc__
    CALL_LOG.append("contract_check")  # => co-17: log this stage's participation -- happens BEFORE any downstream read
    return "amount" in row  # => co-17: the SAME kind of check ex-39 built, run at the earliest possible point


def downstream_read(row: dict[str, object]) -> str:  # => co-17: a downstream consumer -- should NEVER be reached if the contract failed
    """A downstream consumer reading this row -- must never execute against a contract-violating row."""  # => co-17: documents downstream_read's contract -- no runtime output, just sets its __doc__
    CALL_LOG.append("downstream_read")  # => co-17: log this stage's participation -- reached ONLY if the contract passed
    return f"processing order {row['order_id']}"  # => co-17: only safe to run once the contract has already been verified


if __name__ == "__main__":  # => co-17: entry point -- runs only when this file executes directly, not on import
    row = produce_row()  # => co-17: stage 1 -- PRODUCE
    contract_ok = check_contract_at_produce_time(row)  # => co-17: stage 2 -- CONTRACT CHECK, co-located right after produce
    print(f"Call order so far: {CALL_LOG} | Contract passed: {contract_ok}")  # => co-17: prints the call order and the contract's verdict
    if contract_ok:  # => co-17: downstream_read runs ONLY if the contract passed -- gated, not unconditional
        downstream_read(row)  # => co-17: this line must NOT execute for a drifted row
    print(f"Final call order: {CALL_LOG}")  # => co-17: prints the complete, final call order

    assert CALL_LOG == ["produce", "contract_check"], "downstream_read must never run once the contract check fails"  # => co-17: the claim
    assert contract_ok is False, "this deliberately drifted row must fail its contract check"  # => co-17: sanity check on the fixture
    print("MATCH: the contract check ran immediately after produce, and downstream_read never executed on the drifted row")  # => co-17
    # => co-17: co-locating the check with the producer is what catches drift at its SOURCE, before ANY downstream reader is exposed
