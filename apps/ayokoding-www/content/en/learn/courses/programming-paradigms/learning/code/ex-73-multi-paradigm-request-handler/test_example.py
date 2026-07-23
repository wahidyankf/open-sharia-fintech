"""Example 73: pytest verification for Multi-Paradigm Request Handler."""

from example import RequestRouter, compute_summary


def test_request_handled_end_to_end_across_all_three_layers() -> None:
    router = RequestRouter()  # => fresh router, isolated from the module-level demo
    router.handle("create", "ord-x", ["a"])  # => event-driven entry point
    result = router.handle("ship", "ord-x")  # => OO mutation via mark_shipped()
    assert "status=shipped" in result  # => functional core correctly reports the OO mutation
    assert router.handled == ["create:ord-x", "ship:ord-x"]  # => event-driven shell recorded both events


def test_functional_core_is_independently_testable_with_no_router_at_all() -> None:
    from example import Order

    order = Order("standalone", ["x", "y", "z"])  # => construct an OO object directly, no router involved
    assert compute_summary(order) == "Order standalone: 3 item(s), status=pending"  # => pure function, no I/O


# => Run: pytest -- Output: 2 passed
