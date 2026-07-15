"""Capstone Step 1 + Step 2: TDD'd unit tests for compute_subtotal(), plus a stubbed TaxGateway."""
# Step 1's three tests below were written BEFORE compute_subtotal() existed (see the capstone
# overview's Run block for the genuine red-then-green transcript). Step 2's test isolates
# TaxGateway -- an external dependency -- with a stub, so compute_order_total() runs with NO
# real network call at all.

from __future__ import (
    annotations,
)  # => enables modern union/generic syntax under this pinned Python

from unittest.mock import MagicMock  # => co-12/co-13: the ONE double type this file's Step 2 uses  # fmt: skip

from service import TaxGateway, compute_order_total, compute_subtotal  # => co-01: the REAL logic under test  # fmt: skip

# ---------------------------------------------------------------------------
# Step 1: TDD unit tests for the PURE function -- red first, then made to pass minimally.
# ---------------------------------------------------------------------------


def test_unit_subtotal_of_empty_list_is_zero() -> None:  # => co-17: the FIRST test written, red first  # fmt: skip
    assert compute_subtotal([]) == 0  # => co-01: the trivial base case -- zero items, zero total  # fmt: skip


def test_unit_subtotal_of_single_item() -> None:  # => co-17: the SECOND test, red against a stub impl  # fmt: skip
    assert compute_subtotal([9.99]) == 9.99  # => co-01: one item passes through unchanged  # fmt: skip


def test_unit_subtotal_of_multiple_items_rounds_to_cents() -> None:  # => co-17: the THIRD test  # fmt: skip
    assert compute_subtotal([0.10, 0.20]) == 0.30  # => pins down float-rounding behavior too  # fmt: skip


# ---------------------------------------------------------------------------
# Step 2: a stub/mock TaxGateway isolates compute_order_total() from any real dependency.
# ---------------------------------------------------------------------------


def test_unit_order_total_uses_stubbed_tax_rate_no_real_gateway_called() -> (
    None
):  # => co-12
    stub_gateway = MagicMock(spec=TaxGateway)  # => co-12: spec= constrains it to TaxGateway's shape  # fmt: skip
    stub_gateway.rate_for_region.return_value = 0.08  # => co-12: a CANNED 8% rate -- no real call  # fmt: skip

    total = compute_order_total(
        [10.00, 20.00], region="US-CA", tax_gateway=stub_gateway
    )  # => co-01/co-12

    assert total == 32.40  # => 30.00 * 1.08, computed WITHOUT any real external tax API call  # fmt: skip
    stub_gateway.rate_for_region.assert_called_once_with("US-CA")  # => co-13: confirms the ISOLATED  # fmt: skip
    # => dependency WAS consulted (the interaction happened) -- just never for real, over the network


def test_unit_order_total_zero_rate_leaves_subtotal_unchanged() -> None:  # => a SECOND stub scenario  # fmt: skip
    stub_gateway = MagicMock(spec=TaxGateway)  # => co-12: a FRESH stub, independent of the test above  # fmt: skip
    stub_gateway.rate_for_region.return_value = 0.0  # => co-12: a DIFFERENT canned rate, still no real call  # fmt: skip

    total = compute_order_total(
        [50.00], region="US-OR", tax_gateway=stub_gateway
    )  # => co-01/co-12: combined

    assert total == 50.00  # => 0% tax means the subtotal passes through unchanged  # fmt: skip
