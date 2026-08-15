"""Adapters sit outside the capstone domain package."""

from dataclasses import dataclass

from domain.model import Order, OrderRepository


class MemoryOrderRepository(OrderRepository):
    def __init__(self) -> None:
        self._orders: dict[str, Order] = {}

    def add(self, order: Order) -> None:
        self._orders[order.order_id] = order

    def get(self, order_id: str) -> Order:
        return self._orders[order_id]


@dataclass(frozen=True)
class LegacyOrderDTO:
    client_order_number: str
    units: int


@dataclass(frozen=True)
class ShippingRequest:
    sales_order_id: str
    quantity: int


def legacy_to_shipping(dto: LegacyOrderDTO) -> ShippingRequest:
    """ACL: both legacy field names and sales vocabulary end at this function."""
    return ShippingRequest(sales_order_id=dto.client_order_number, quantity=dto.units)
