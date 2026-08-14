"""Worked Example 4: define application policy against a port."""

from typing import Protocol


class Notifier(Protocol):
    def send(self, message: str) -> None: ...


class PrintNotifier:
    def send(self, message: str) -> None:
        print(message)


def confirm_order(notifier: Notifier, order_id: str) -> None:
    notifier.send(f"confirmed {order_id}")


confirm_order(PrintNotifier(), "order-1")
