"""Thin orchestration layer for the capstone."""

from domain.model import Order, OrderPlaced, OrderRepository


def place_order(order: Order, repository: OrderRepository) -> list[OrderPlaced]:
    order.place()
    repository.add(order)
    events = order.pending_events[:]
    order.pending_events.clear()
    return events
