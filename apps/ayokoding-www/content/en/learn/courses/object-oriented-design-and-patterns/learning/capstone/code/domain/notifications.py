"""Capstone Step 3: NotificationLog -- a concrete Observer, decoupled from OrderEngine.

co-26 (Observer): implements the OrderPlacedObserver protocol structurally -- OrderEngine
never imports this class by name, only the protocol it satisfies.
"""

from __future__ import annotations


class NotificationLog:  # => SRP: notification, and only notification -- a separate reason to change from pricing
    def __init__(self) -> None:
        self.messages: list[str] = []

    def on_order_placed(self, total: float) -> None:
        self.messages.append(f"order checked out: total {total:.2f}")
