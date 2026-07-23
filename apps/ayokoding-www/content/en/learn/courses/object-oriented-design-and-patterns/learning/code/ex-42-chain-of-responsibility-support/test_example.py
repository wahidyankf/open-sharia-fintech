"""Example 42: pytest verification for Escalating a Ticket Through a Handler Chain."""

from example import L1Handler, L2Handler, L3Handler


def _build_chain() -> L1Handler:
    l1, l2, l3 = L1Handler(), L2Handler(), L3Handler()
    l1.set_next(l2).set_next(l3)
    return l1


def test_ticket_handled_at_the_first_capable_tier() -> None:
    assert _build_chain().handle(1) == "resolved at L1"  # => no escalation needed


def test_unhandled_ticket_at_l1_falls_to_the_next_handler() -> None:
    assert _build_chain().handle(2) == "resolved at L2"  # => L1 rejects it, L2 resolves it


def test_ticket_beyond_every_tier_reports_unhandled() -> None:
    assert _build_chain().handle(9) == "unhandled: no tier could resolve this ticket"  # => fell off the end of the chain


# => Run: pytest -- Output: 3 passed
