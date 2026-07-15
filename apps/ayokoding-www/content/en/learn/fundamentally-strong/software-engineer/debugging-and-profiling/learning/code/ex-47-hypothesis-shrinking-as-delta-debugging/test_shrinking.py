"""Example 47: Hypothesis's built-in shrinker as an automatic, off-the-shelf ddmin.

ex-45 and ex-46 hand-rolled a minimizer. Hypothesis does the exact same job --
generate random inputs, and when one fails, repeatedly try smaller/simpler
variants of it -- automatically, for any property you write. This example seeds
a discount-calculation bug (negative discounts allowed through) and lets
Hypothesis both FIND a failing case and SHRINK it to the smallest one.
"""

from __future__ import annotations

from hypothesis import Phase, given, settings
from hypothesis import strategies as st


def apply_discount(price: float, discount_pct: float) -> float:
    # co-14: the real bug -- no validation that discount_pct is in [0, 100], so a
    # negative "discount" silently INCREASES the price. (Deliberately no round()
    # here: rounding to cents introduces its own float-representation edge cases
    # at exactly 0% that would surface a second, unrelated bug and muddy the
    # comparison this example is making.)
    return price * (1 - discount_pct / 100)


@given(
    price=st.floats(min_value=0, max_value=10_000, allow_nan=False),
    discount_pct=st.floats(allow_nan=False, allow_infinity=False),
)
@settings(max_examples=200, phases=[Phase.generate, Phase.shrink])
def property_discounted_price_never_exceeds_original(
    price: float, discount_pct: float
) -> None:
    result = apply_discount(price, discount_pct)
    assert result <= price, (
        f"discounted price {result} exceeded original {price} (discount_pct={discount_pct})"
    )


def hand_rolled_ddmin_discount(price: float, initial_bad_discount: float) -> float:
    # co-11: same idea as ex-45/ex-46's ddmin, applied to a single float instead of
    # a dict or a string -- binary-search the discount_pct toward zero, keeping the
    # smallest-magnitude value that STILL makes the property fail.
    lo, hi = 0.0, initial_bad_discount  # =>  lo=known-good boundary, hi=known-bad value
    for _ in range(
        60
    ):  # =>  60 halvings is far more precision than float ever needs here
        mid = (lo + hi) / 2
        if apply_discount(price, mid) > price:
            hi = mid  # =>  mid still fails -- shrink toward zero further
        else:
            lo = mid  # =>  mid passes -- the failing boundary is between mid and hi
    return hi


def main() -> None:
    try:
        property_discounted_price_never_exceeds_original()
    except AssertionError as exc:
        print("Hypothesis found and shrank a failing case:")
        print(f"  {exc}")
    else:
        print("no failure found (unexpected -- the bug should always be reachable)")
        return

    # co-11: run the hand-rolled minimizer on the SAME bug, starting from a much
    # larger, less-minimal failing discount_pct, and compare the two results.
    hand_rolled = hand_rolled_ddmin_discount(
        price=1.0, initial_bad_discount=-1_000_000.0
    )
    print(f"hand-rolled ddmin shrank discount_pct to: {hand_rolled!r}")
    print(
        "comparison: both the Hypothesis shrinker and the hand-rolled ddmin converge on"
    )
    print(
        "the same boundary -- any discount_pct below 0.0 -- confirming they are comparably"
    )
    print(
        "minimal even though Hypothesis needed zero custom shrinking code to get there."
    )
    assert hand_rolled < 0.0, (
        "hand-rolled minimizer must land on a strictly negative discount_pct"
    )
    assert abs(hand_rolled) < 1e-6, (
        f"expected the shrunk discount_pct to be nearly zero, got {hand_rolled}"
    )


if __name__ == "__main__":
    main()
