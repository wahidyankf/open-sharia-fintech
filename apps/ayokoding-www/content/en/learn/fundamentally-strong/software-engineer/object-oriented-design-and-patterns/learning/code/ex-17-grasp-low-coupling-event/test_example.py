"""Example 17: pytest verification for Low Coupling: Decouple via an Event Bus."""

import inspect

from example import EventBus, InventoryModule, OrderModule


def test_neither_module_names_the_other_in_its_own_source() -> None:
    order_source: str = inspect.getsource(OrderModule)  # => OrderModule's own source only
    inventory_source: str = inspect.getsource(InventoryModule)  # => and vice versa
    assert "InventoryModule" not in order_source  # => zero coupling in one direction
    assert "OrderModule" not in inventory_source  # => zero coupling in the other direction


def test_placing_an_order_still_updates_inventory_via_the_bus() -> None:
    bus: EventBus = EventBus()
    inventory: InventoryModule = InventoryModule(bus)
    order_module: OrderModule = OrderModule(bus)
    order_module.place_order(10)  # => the only call OrderModule ever makes
    assert inventory.stock == 90  # => the event still reached InventoryModule


# => Run: pytest -- Output: 2 passed
