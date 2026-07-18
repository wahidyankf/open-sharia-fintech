# learning/code/ex-49-debt-driven-refactor-with-flag/debt_refactor.py
"""ex-49: paying down DEBT-041 behind a flag -- old and new paths COEXIST until verified (co-16, co-22, co-14)."""  # => co-16: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

from dataclasses import dataclass  # => co-14: a tiny typed record stands in for a real database row


@dataclass  # => co-14: mutable on purpose -- balance changes are the whole point of a redemption
class CardBalance:  # => co-16: the record DEBT-041 (Example 28) flagged as missing concurrency protection
    balance: float  # => co-16: the field the old, unlocked path can race on
    locked: bool = False  # => co-16: NEW -- the new path's own lock flag, absent from the old path entirely


def redeem_old_path(card: CardBalance, amount: float) -> float:  # => co-16: the ORIGINAL, unlocked implementation
    """Redeem without any concurrency protection -- exactly DEBT-041's logged gap."""  # => co-16: documents redeem_old_path's contract -- no runtime output, just sets its __doc__
    card.balance -= amount  # => co-16: no lock check -- two concurrent calls could both pass this line before either writes
    return card.balance  # => co-16: returns this computed value to the caller


def redeem_new_path(card: CardBalance, amount: float) -> float:  # => co-14: the REFACTORED implementation, paying down DEBT-041
    """Redeem with a simple lock flag -- the fix DEBT-041's log entry scoped and estimated."""  # => co-14: documents redeem_new_path's contract -- no runtime output, just sets its __doc__
    if card.locked:  # => co-14: a concurrent call finds the card already mid-redemption
        raise RuntimeError("card is locked -- a redemption is already in progress")  # => co-14: rejects instead of racing
    card.locked = True  # => co-14: acquires the lock -- the gap DEBT-041 named is closed HERE
    try:  # => co-14: ensures the lock is released even if something below raises
        card.balance -= amount  # => co-14: the SAME arithmetic as the old path -- only the concurrency safety differs
        return card.balance  # => co-14: returns this computed value to the caller
    finally:  # => co-14: guarantees release regardless of success or failure above
        card.locked = False  # => co-14: releases the lock -- the next redemption call can proceed


def redeem(card: CardBalance, amount: float, *, new_path_enabled: bool) -> float:  # => co-22: the FLAG-gated entry point
    """Route to the old or new redemption path, controlled by the new_path_enabled flag."""  # => co-22: documents redeem's contract -- no runtime output, just sets its __doc__
    if new_path_enabled:  # => co-22: the flag itself -- BOTH paths remain in the codebase, coexisting
        return redeem_new_path(card, amount)  # => co-22: the new, refactored path
    return redeem_old_path(card, amount)  # => co-22: the OLD path, still present, still reachable with the flag off


if __name__ == "__main__":  # => co-22: entry point -- this block runs only when the file executes directly, not on import
    old_card = CardBalance(balance=100.0)  # => co-16: a fresh card for the OLD path
    old_result = redeem(old_card, 30.0, new_path_enabled=False)  # => co-22: flag OFF -- exercises redeem_old_path
    print(f"old path (flag off): balance={old_result}, locked={old_card.locked}")  # => co-16: locked stays False -- old path never sets it

    new_card = CardBalance(balance=100.0)  # => co-14: a fresh card for the NEW path
    new_result = redeem(new_card, 30.0, new_path_enabled=True)  # => co-22: flag ON -- exercises redeem_new_path
    print(f"new path (flag on):  balance={new_result}, locked={new_card.locked}")  # => co-14: locked is False AGAIN -- released after use

    assert old_result == new_result == 70.0, "both paths must compute the SAME arithmetic result"  # => co-14: correctness check
    concurrent_card = CardBalance(balance=100.0, locked=True)  # => co-14: simulates a redemption ALREADY in progress
    try:  # => co-14: the new path's own protection, under test
        redeem(concurrent_card, 10.0, new_path_enabled=True)  # => co-14: expected to be REJECTED, not raced
        raise AssertionError("expected RuntimeError for a locked card")  # => co-14: fails loudly if the gate did not fire
    except RuntimeError:  # => co-14: expected -- the gate is doing its job
        print("new path correctly REJECTS a concurrent redemption attempt")  # => co-14: prints the confirmation
    print("Old and new paths coexist behind the flag, both verified independently: True")  # => co-16, co-22, co-14: reached only if every assert/except above held
