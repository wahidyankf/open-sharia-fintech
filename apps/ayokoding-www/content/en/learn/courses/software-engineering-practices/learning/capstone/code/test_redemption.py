# learning/capstone/code/test_redemption.py
"""The failing test written BEFORE redemption.py's real implementation existed (the RED step)."""  # => this file's own restated purpose, doubling as its module __doc__
# => no runtime output beyond setting __doc__ -- the line above just orients the reader

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

import pytest  # => pytest.raises -- the standard way to assert an expected exception, used below

from redemption import redeem_points  # => imports the SAME function this test drove into existence


def test_redeem_within_cap_succeeds() -> None:  # => the "happy path" case -- a request under the cap is honored exactly
    # A cart worth 100.0 allows redeeming up to 50.0 points (the 50% cap) --  # => states the fixture's own reasoning, not just its numbers
    # 40.0 is comfortably under that limit.
    assert redeem_points(cart_subtotal=100.0, points_requested=40.0) == 40.0  # => the function must return the request UNCHANGED when it fits


def test_redeem_above_cap_raises() -> None:  # => the case that actually drives the cap's existence
    with pytest.raises(ValueError):  # => 60.0 exceeds 50% of 100.0 -- the cap MUST reject this, not silently clamp it
        redeem_points(cart_subtotal=100.0, points_requested=60.0)  # => expected to raise -- pytest.raises fails the test if it does not
