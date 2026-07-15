"""Example 63: Test Two Real Collaborating Modules Together, No Stub at the Seam."""
# Neither module below is ever replaced with a stub or mock -- co-23's defining trait is that
# the SEAM between InventoryService and OrderService stays real, end to end, in every test.

from __future__ import (
    annotations,
)  # => enables modern union/generic syntax under this pinned Python


class InventoryService:  # => module 1 -- owns stock levels, nothing else knows its internals  # fmt: skip
    """Tracks how many units of each SKU are in stock."""  # => co-23: the FIRST real module  # fmt: skip

    def __init__(self, stock: dict[str, int]) -> None:  # => seeds the starting inventory  # fmt: skip
        self._stock = dict(stock)  # => a COPY -- callers can't mutate the constructor's dict later  # fmt: skip

    def available(self, sku: str) -> int:  # => co-23: OrderService will call this for REAL below  # fmt: skip
        return self._stock.get(sku, 0)  # => 0 for an unknown SKU, never a KeyError  # fmt: skip

    def reserve(self, sku: str, quantity: int) -> bool:  # => decrements stock, returns success  # fmt: skip
        if self._stock.get(sku, 0) < quantity:  # => not enough stock -- refuse, don't go negative  # fmt: skip
            return False  # => co-23: the REAL refusal path OrderService reacts to below  # fmt: skip
        self._stock[sku] -= quantity  # => the REAL side effect OrderService depends on  # fmt: skip
        return True  # => co-23: the REAL success path  # fmt: skip


class OrderService:  # => module 2 -- co-23: depends on a REAL InventoryService, not a mock  # fmt: skip
    """Places orders against a real InventoryService -- the SEAM this example refuses to stub."""  # => co-23

    def __init__(self, inventory: InventoryService) -> None:  # => co-23: the collaborator is REAL  # fmt: skip
        self.inventory = inventory  # => stored as-is -- no stub/mock ever substituted for it  # fmt: skip

    def place_order(self, sku: str, quantity: int) -> str:  # => the combined, cross-module behavior  # fmt: skip
        if self.inventory.reserve(sku, quantity):  # => a REAL call into the OTHER real module  # fmt: skip
            return "confirmed"  # => co-23: the REAL, cross-module success outcome  # fmt: skip
        return "rejected: insufficient stock"  # => co-23: the REAL, cross-module refusal outcome  # fmt: skip


def test_integration_order_confirmed_when_stock_sufficient() -> (
    None
):  # => co-23: BOTH modules, real
    inventory = InventoryService({"widget": 10})  # => a REAL InventoryService, seeded with stock  # fmt: skip
    orders = OrderService(inventory)  # => co-23: OrderService wired to the REAL inventory above  # fmt: skip
    result = orders.place_order("widget", 3)  # => this call crosses the module seam, unstubbed  # fmt: skip
    assert result == "confirmed"  # => confirms the CROSS-MODULE decision came back correct  # fmt: skip
    assert inventory.available("widget") == 7  # => confirms the REAL side effect landed in module 1  # fmt: skip


def test_integration_order_rejected_when_stock_insufficient() -> None:  # => the OTHER real branch  # fmt: skip
    inventory = InventoryService({"widget": 2})  # => a REAL InventoryService, low stock  # fmt: skip
    orders = OrderService(inventory)  # => co-23: wired to the SAME real inventory  # fmt: skip
    result = orders.place_order("widget", 5)  # => asks for MORE than is genuinely available  # fmt: skip
    assert result == "rejected: insufficient stock"  # => the real reserve() call refused, honestly  # fmt: skip
    assert inventory.available("widget") == 2  # => confirms NOTHING was decremented on rejection  # fmt: skip


def test_integration_two_orders_in_sequence_share_real_state() -> (
    None
):  # => state persists ACROSS calls
    inventory = InventoryService({"widget": 5})  # => a REAL InventoryService, starting stock of 5  # fmt: skip
    orders = OrderService(inventory)  # => co-23: ONE OrderService, reused for TWO calls below  # fmt: skip
    first = orders.place_order("widget", 3)  # => the FIRST real call, decrementing real state  # fmt: skip
    second = orders.place_order("widget", 3)  # => the SECOND call sees the FIRST call's real effect  # fmt: skip
    assert first == "confirmed"  # => 5 - 3 = 2 remaining, so this one succeeds  # fmt: skip
    assert second == "rejected: insufficient stock"  # => only 2 left, asked for 3 -- a REAL conflict  # fmt: skip
