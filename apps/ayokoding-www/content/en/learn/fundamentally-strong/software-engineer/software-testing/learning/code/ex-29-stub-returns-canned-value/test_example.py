# learning/code/ex-29-stub-returns-canned-value/test_example.py
"""Example 29: A Stub Returns a Canned Value."""

import pytest  # => pytest.approx -- 100.0 * 1.10 has real float error (co-07), unrelated to stubbing itself  # fmt: skip


# ex-29: a STUB is a double that returns a FIXED, canned answer -- no logic, no recording (co-12, co-11)  # fmt: skip
class StubTaxRateProvider:  # => a stub: implements the SAME interface a real provider would  # fmt: skip
    def get_rate(
        self, region: str
    ) -> float:  # => region is accepted but IGNORED entirely
        return 0.10  # => always returns the SAME canned 10% rate, regardless of the real region  # fmt: skip


def calculate_total(amount: float, region: str, tax_provider) -> float:  # => the unit under test  # fmt: skip
    rate = tax_provider.get_rate(region)  # => depends on a COLLABORATOR, not a real tax service  # fmt: skip
    return amount * (1 + rate)  # => applies whatever rate the collaborator handed back


def test_calculate_total_uses_the_stubbed_rate() -> None:
    stub = StubTaxRateProvider()  # => arrange: the canned-answer double, no real tax service involved  # fmt: skip
    total = calculate_total(100.0, region="anywhere", tax_provider=stub)  # => act  # fmt: skip
    assert total == pytest.approx(110.0)  # => 100 * (1 + 0.10) -- approx absorbs float error (co-07)  # fmt: skip
    # => calculate_total never knows OR cares that get_rate's answer is canned -- the stub's
    # => whole job is to make the unit runnable in isolation from a real tax service (co-12)
