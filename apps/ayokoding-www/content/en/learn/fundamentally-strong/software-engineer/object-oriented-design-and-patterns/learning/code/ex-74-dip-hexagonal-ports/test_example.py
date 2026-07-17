"""Example 74: pytest verification of the hexagonal ports-and-adapters wiring."""

from example import (
    EmailAdapter,
    OrderDomain,
    SmsAdapter,
    domain_module_imports_no_infrastructure_names,
)


def test_domain_confirms_an_order_through_the_email_adapter() -> None:
    email = EmailAdapter()
    domain = OrderDomain(email)
    domain.confirm_order("ord-1")
    assert email.sent == ["[email] order ord-1 confirmed"]


def test_swapping_the_adapter_needs_no_edit_to_order_domain() -> None:
    sms = SmsAdapter()
    domain = OrderDomain(sms)  # => same OrderDomain class, a DIFFERENT adapter -- zero source changes
    domain.confirm_order("ord-2")
    assert sms.sent == ["[sms] order ord-2 confirmed"]


def test_order_domain_depends_on_the_port_not_a_concrete_adapter() -> None:
    assert domain_module_imports_no_infrastructure_names()  # => co-05: the dependency direction points inward


# => Run: pytest -q -- Output: 3 passed
