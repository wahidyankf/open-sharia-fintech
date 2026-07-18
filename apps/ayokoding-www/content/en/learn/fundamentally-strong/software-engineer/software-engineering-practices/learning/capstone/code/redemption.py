# learning/capstone/code/redemption.py
"""Capstone: cap a points redemption at 50% of the cart subtotal.

The FINAL implementation, after the RED -> GREEN -> REFACTOR loop shown in
tdd-and-history.sh (a prerequisite skill from topic 15, Software Testing --
this topic does not re-teach TDD mechanics, only applies them). This file is
what the clean "feat(loyalty): ..." commit actually contains.
"""  # => this file's own restated purpose, doubling as its module __doc__
# => no runtime output beyond setting __doc__ -- the paragraph above just orients the reader

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

MAX_REDEMPTION_FRACTION = 0.5  # => the business rule, named -- a reviewer reads THIS constant, not a bare "0.5" inline


def redeem_points(cart_subtotal: float, points_requested: float) -> float:  # => the ONE function the whole capstone TDD loop targets
    """Return points_requested if it is within the cap, else raise ValueError.

    Raises:
        ValueError: if points_requested exceeds MAX_REDEMPTION_FRACTION of cart_subtotal.
    """  # => documents redeem_points's contract -- no runtime output, just sets its __doc__
    if points_requested > cart_subtotal * MAX_REDEMPTION_FRACTION:  # => the cap check -- the SAME rule test_redeem_above_cap_raises exercises
        raise ValueError(  # => a caller-legible error, not a silent clamp -- the caller decides how to handle an over-cap request
            f"points_requested={points_requested} exceeds the "  # => names BOTH values -- easier to debug than a bare "over cap" string
            f"{MAX_REDEMPTION_FRACTION:.0%} cap of cart_subtotal={cart_subtotal}"
        )  # => closes the multi-line construct opened above
    return points_requested  # => within the cap -- the request is honored exactly as asked, no partial redemption


if __name__ == "__main__":  # => entry point -- this block runs only when the file executes directly, not on import
    print(f"redeem_points(100.0, 40.0) = {redeem_points(100.0, 40.0)}")  # => within the 50-point cap -- succeeds
    try:  # => demonstrates the cap's own error path, not just its success path
        redeem_points(100.0, 60.0)  # => 60 exceeds 50% of 100 -- expected to raise
        raise AssertionError("expected ValueError for an over-cap redemption")  # => fails loudly if the cap did not fire
    except ValueError as exc:  # => expected -- the cap is doing its job
        print(f"redeem_points(100.0, 60.0) correctly raised: {exc}")  # => prints the caller-legible message constructed above
    print("Capstone Step 1's TDD'd feature behaves as specified: True")  # => reached only if both calls above behaved as expected
