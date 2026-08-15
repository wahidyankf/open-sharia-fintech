# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Worked Example 4: define application policy against a port."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from typing import Protocol


# => This keeps the modeled rule explicit so its trade-off can be inspected.
class Notifier(Protocol):
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    def send(self, message: str) -> None: ...


# => This keeps the modeled rule explicit so its trade-off can be inspected.
class PrintNotifier:
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    def send(self, message: str) -> None:
        # => This keeps the modeled rule explicit so its trade-off can be inspected.
        print(message)


# => This keeps the modeled rule explicit so its trade-off can be inspected.
def confirm_order(notifier: Notifier, order_id: str) -> None:
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    notifier.send(f"confirmed {order_id}")


# => This keeps the modeled rule explicit so its trade-off can be inspected.
confirm_order(PrintNotifier(), "order-1")
