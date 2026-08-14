"""Example 68: generic capability gets a thin adapter, not a rich model."""


class NotificationGateway:
    def send(self, message: str) -> str:
        return f"sent:{message}"  # => generic capability delegates to a provider


catalog_kind = "supporting"  # => catalog helps the core but does not differentiate it

assert (
    NotificationGateway().send("hello") == "sent:hello" and catalog_kind == "supporting"
)
