"""Example 78: Choose the Right Double for the Scenario -- State vs Behavior, Justified."""

from __future__ import (
    annotations,
)  # => enables modern union/generic syntax under this pinned Python

from unittest.mock import MagicMock  # => co-12/co-13: the ONE double type, used for TWO different roles  # fmt: skip


class WelcomeMailer:  # => a real collaborator whose ONLY job is a side effect -- no return value  # fmt: skip
    def send(self, to: str) -> None:  # => co-13: real sends produce NO usable return value at all  # fmt: skip
        raise NotImplementedError(
            "would genuinely email someone -- must never run in a test"
        )  # => co-13


def register_user(
    name: str, email: str, mailer: WelcomeMailer
) -> str:  # => the unit under test #1
    """Registers a user and triggers a welcome email -- the EMAIL SENDING is the interesting part."""  # => co-13
    mailer.send(email)  # => co-13: the entire reason this scenario is worth testing at all  # fmt: skip
    return f"registered:{name}"  # => co-13: the STATE half of this function's contract  # fmt: skip


class DiscountCalculator:  # => a real collaborator whose RESULT is what matters, not how it's called
    def rate_for(self, tier: str) -> float:  # => co-12: a lookup whose RETURN VALUE is the point  # fmt: skip
        raise NotImplementedError(
            "a real rate table -- irrelevant to what THIS test checks"
        )  # => co-12


def price_after_discount(
    base: float, tier: str, calc: DiscountCalculator
) -> float:  # => unit #2
    """Computes a discounted price -- the RESULT is what matters, not how calc was invoked."""  # => co-12
    rate = calc.rate_for(tier)  # => co-12: the CALLER doesn't care how many times/how this ran  # fmt: skip
    return round(base * (1 - rate), 2)  # => co-12: the STATE this whole function exists to produce  # fmt: skip


# ---- Scenario 1: register_user -- co-13 MOCK is correct here, a STUB would be a lie ----
def test_register_user_correctly_uses_a_mock_to_check_behavior() -> (
    None
):  # => co-13: behavior check
    mock_mailer = MagicMock()  # => co-13: a MOCK, chosen because send() has NO return value to check  # fmt: skip
    result = register_user("Asha", "asha@example.com", mock_mailer)  # => act: the ONE call under test  # fmt: skip

    # STATE assertion: proves registration itself worked.
    assert result == "registered:Asha"  # => co-13: the state-based half of this test  # fmt: skip

    # BEHAVIOR assertion: proves the SIDE EFFECT happened -- the ONLY way to know an email was
    # ever attempted at all. A stub here (mailer.send returning some canned value) would let this
    # test pass even if send() were NEVER CALLED -- the mock's call verification is the whole point.
    mock_mailer.send.assert_called_once_with("asha@example.com")  # => co-13: the CORRECT dimension  # fmt: skip


# ---- Scenario 2: price_after_discount -- co-12 STUB is correct here, a MOCK would be noise ----
def test_price_after_discount_correctly_uses_a_stub_to_check_state() -> (
    None
):  # => co-12: state check
    stub_calc = MagicMock()  # => co-12: used as a STUB -- only its RETURN VALUE is configured  # fmt: skip
    stub_calc.rate_for.return_value = 0.20  # => co-12: a CANNED answer, the stub's defining trait  # fmt: skip

    result = price_after_discount(100.0, "gold", stub_calc)  # => act: the ONE call under test  # fmt: skip

    # STATE assertion: the CORRECT dimension for a pure calculation -- the caller only cares
    # about the NUMBER that comes back, not the mechanics of how rate_for() got invoked.
    assert result == 80.0  # => co-12: this is what actually matters for a pricing calculation  # fmt: skip

    # Asserting stub_calc.rate_for.assert_called_once_with("gold") here would ALSO pass, but it
    # would be testing an IMPLEMENTATION DETAIL (that a lookup happened) rather than the actual
    # CONTRACT (that the discount was computed correctly) -- exactly the wrong dimension to pin
    # down for a pure calculation, which is why this test deliberately does NOT assert on it.
