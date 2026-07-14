"""Example 79: pytest verification for A Full Domain Model in One Package."""

import pytest

from example import FlatPricing, Invoice, Money


def test_full_domain_model_computes_correct_total() -> None:
    invoice: Invoice = Invoice(FlatPricing())
    invoice.add_item(Money(500))
    invoice.add_item(Money(300))
    assert invoice.total == Money(800)  # => Money's dataclass __eq__ compares by value


def test_full_domain_model_rejects_negative_line_item() -> None:
    invoice: Invoice = Invoice(FlatPricing())
    with pytest.raises(ValueError):
        invoice.add_item(Money(-1))


# => Run: pytest -- Output: 2 passed
