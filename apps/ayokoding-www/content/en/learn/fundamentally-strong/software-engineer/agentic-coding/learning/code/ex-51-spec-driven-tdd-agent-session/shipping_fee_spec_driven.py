# learning/code/ex-51-spec-driven-tdd-agent-session/shipping_fee_spec_driven.py
"""Example ex-51: Spec-Driven TDD Agent Session -- Red Run, Then Green, Against spec.md's AC Bullets."""  # => co-21: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

from collections.abc import Callable  # => co-14: types the fn parameter run_acceptance_suite is quantified over

# --- THE SPEC (co-21), restated from the colocated spec.md ------------------  # => co-21: spec-driven means the tests below are DERIVED from this, not invented ad hoc
# AC1. subtotal >= 50.00 ships free (fee = 0.00).                              # => co-21: AC bullet 1
# AC2. subtotal < 50.00 pays a flat $5.00 fee.                                  # => co-21: AC bullet 2
# AC3. an express flag adds a $10.00 surcharge on top of AC1/AC2's result.      # => co-21: AC bullet 3
# AC4. the fee is always a non-negative float, rounded to 2 decimal places.     # => co-21: AC bullet 4
# ------------------------------------------------------------------------------


def shipping_fee_v1_incomplete(subtotal: float, express: bool = False) -> float:  # => co-14: the RED state -- pre-agent stub, ignores AC1 and AC3
    """Incomplete stub: always charges a flat $5.00, ignoring the free-shipping threshold."""  # => co-14: documents the (incomplete) contract this stub actually implements
    return 5.00  # => co-14: BUG per AC1 -- never returns 0.00, even when subtotal >= 50.00; also ignores AC3's express surcharge


def shipping_fee_v2_spec_compliant(subtotal: float, express: bool = False) -> float:  # => co-14: the GREEN state -- the agent's spec-driven implementation
    """Spec-compliant implementation, satisfying AC1 through AC4."""  # => co-14: documents the contract this diff actually implements
    base = 0.00 if subtotal >= 50.00 else 5.00  # => co-21: AC1 + AC2 in one expression
    surcharge = 10.00 if express else 0.00  # => co-21: AC3 -- added on top of `base`, whichever branch fired
    fee = base + surcharge  # => co-21: combines AC1/AC2's base with AC3's surcharge
    return round(max(fee, 0.00), 2)  # => co-21: AC4 -- non-negative, rounded to 2 decimals


def run_acceptance_suite(name: str, fn: Callable[..., float]) -> bool:  # => co-14: runs all four AC checks against `fn`; returns True only if every one passes
    """Check `fn` against AC1-AC4; print + return False on the first failing bullet."""  # => co-14: documents run_acceptance_suite's contract
    checks = [  # => co-14: one tuple per AC bullet -- (label, actual, expected)
        ("AC1 (>=50 ships free)", fn(75.00), 0.00),  # => co-21: AC1's exact case
        ("AC2 (<50 flat $5)", fn(20.00), 5.00),  # => co-21: AC2's exact case
        ("AC3 (express surcharge)", fn(75.00, express=True), 10.00),  # => co-21: AC3's exact case -- free base + surcharge
        ("AC4 (non-negative float)", fn(20.00) >= 0.00, True),  # => co-21: AC4's exact case
    ]  # => co-14: closes the checks list
    all_passed = True  # => co-14: tracks whether every bullet held
    for label, actual, expected in checks:  # => co-14: walks every AC bullet in order
        passed = actual == expected  # => co-14: this bullet's pass/fail
        all_passed = all_passed and passed  # => co-14: the suite as a whole only passes if every bullet does
        status = "PASS" if passed else "FAIL"  # => co-14: human-readable label for the transcript
        print(f"{name} -- {label}: {status} (got {actual}, expected {expected})")  # => co-14: one printed line per AC bullet
    return all_passed  # => co-14: True only if every bullet passed


if __name__ == "__main__":  # => co-14: entry point -- this block runs only when the file executes directly, not on import
    print("=== RED: running the acceptance suite against the pre-agent stub ===")  # => co-14: labels the initial red run
    red_result = run_acceptance_suite("shipping_fee_v1_incomplete", shipping_fee_v1_incomplete)  # => co-14: the RED run
    assert red_result is False, "the incomplete stub must FAIL at least one AC bullet"  # => co-14: confirms the red run was genuinely red
    print()  # => co-14: blank line, purely for transcript readability
    print("=== GREEN: running the SAME suite against the spec-compliant implementation ===")  # => co-14: labels the final green run
    green_result = run_acceptance_suite("shipping_fee_v2_spec_compliant", shipping_fee_v2_spec_compliant)  # => co-14: the GREEN run
    assert green_result is True, "the spec-compliant implementation must pass every AC bullet"  # => co-14: confirms the green run was genuinely green
    print("\nAll four spec.md AC bullets pass against the final implementation: True")  # => co-21: reached only if every assert above passed
