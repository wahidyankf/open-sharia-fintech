"""Capstone: order-total service -- a pure subtotal function plus a tax-gateway-dependent total."""
# This one file underpins all four capstone steps: Step 1 TDDs compute_subtotal() from a failing
# test; Step 2 isolates TaxGateway with a stub/mock; Step 3's property test asserts an invariant
# over compute_order_total(); Step 4's app.py (a sibling file) exposes both over real HTTP.

from __future__ import (
    annotations,
)  # => enables modern union/generic syntax under this pinned Python

from abc import ABC, abstractmethod  # => co-12: ABC gives TaxGateway a real, enforceable interface  # fmt: skip


def compute_subtotal(prices: list[float]) -> float:  # => Step 1: TDD'd from a failing test first  # fmt: skip
    """Pure function -- sums a list of line-item prices. No IO, no collaborators."""  # => co-01
    return round(sum(prices), 2)  # => rounds to cents -- the ONLY behavior Step 1's tests pin down  # fmt: skip


class TaxGateway(ABC):  # => Step 2: the EXTERNAL dependency -- a real implementation would call out  # fmt: skip
    """Represents an external tax-rate lookup (e.g. a real HTTP call to a tax API)."""  # => co-12

    @abstractmethod  # => co-12: forces every subclass to implement rate_for_region() -- no silent stub  # fmt: skip
    def rate_for_region(
        self, region: str
    ) -> float:  # => never implemented HERE -- see RealTaxGateway
        raise NotImplementedError  # => co-12: the ABSTRACT method body -- callers must subclass this  # fmt: skip


class RealTaxGateway(TaxGateway):  # => the PRODUCTION implementation -- never touched by any test  # fmt: skip
    """The real gateway -- would genuinely call an external tax-rate API. Not used in tests."""  # => co-12

    def rate_for_region(self, region: str) -> float:  # => the REAL, production-only implementation  # fmt: skip
        raise NotImplementedError(
            "would call a real external tax-rate API -- never in tests"
        )  # => co-12


def compute_order_total(
    prices: list[float], region: str, tax_gateway: TaxGateway
) -> float:  # => Step 3
    """Combines the pure subtotal with an EXTERNAL tax rate -- the dependency Step 2 isolates."""  # => co-23
    subtotal = compute_subtotal(prices)  # => co-01: reuses Step 1's pure function directly  # fmt: skip
    rate = tax_gateway.rate_for_region(region)  # => co-12/co-13: the ISOLATED external call  # fmt: skip
    return round(subtotal * (1 + rate), 2)  # => co-18: the invariant Step 3's property test checks  # fmt: skip
