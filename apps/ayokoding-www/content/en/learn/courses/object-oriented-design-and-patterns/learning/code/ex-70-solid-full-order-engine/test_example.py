"""Example 70: pytest verification of each SOLID seam in the order engine."""

from example import (
    InMemoryRepository,
    NoDiscount,
    Order,
    OrderCalculator,
    OrderService,
    ReceiptFormatter,
    TenPercentOff,
)


def test_srp_each_class_has_exactly_one_reason_to_change() -> None:
    assert not hasattr(OrderCalculator(), "save")  # => pricing never touches persistence
    assert not hasattr(InMemoryRepository(), "total")  # => persistence never touches pricing
    assert not hasattr(ReceiptFormatter(), "apply")  # => formatting never touches discounting


def test_ocp_a_new_discount_is_added_without_editing_order_calculator() -> None:
    order = Order(items={"Book": 20.0, "Pen": 5.0})
    calculator = OrderCalculator()
    assert calculator.total(order, NoDiscount()) == 25.0
    assert calculator.total(order, TenPercentOff()) == 22.5  # => new strategy, zero edits to OrderCalculator.total


def test_lsp_any_discount_strategy_substitutes_for_another_without_breaking_the_caller() -> None:
    order = Order(items={"Book": 20.0})
    calculator = OrderCalculator()
    for discount in (NoDiscount(), TenPercentOff()):  # => both honor "never return more than subtotal"
        assert calculator.total(order, discount) <= 20.0  # => the contract every substitutable strategy must satisfy


def test_isp_order_service_depends_on_only_the_narrow_save_method() -> None:
    repository = InMemoryRepository()
    assert not hasattr(repository, "delete") and not hasattr(repository, "update")  # => no fat interface exists here
    assert hasattr(repository, "save")  # => exactly the one method OrderService's Repository protocol needs


def test_dip_order_service_never_constructs_a_concrete_repository_itself() -> None:
    order = Order(items={"Book": 20.0})
    repository = InMemoryRepository()  # => constructed OUTSIDE OrderService and injected in
    service = OrderService(OrderCalculator(), repository)
    total = service.checkout("ord-1", order, NoDiscount())
    assert total == 20.0
    assert repository.saved == {"ord-1": 20.0}  # => persistence happened through the injected abstraction


# => Run: pytest -q -- Output: 5 passed
