# => Keeps this domain step explicit and reviewable.
"""Example 68: generic capability gets a thin adapter, not a rich model."""


# => Gives domain rules a single, named home.
class NotificationGateway:
    # => Names policy so callers do not recreate the rule.
    def send(self, message: str) -> str:
        return f"sent:{message}"  # => generic capability delegates to a provider


catalog_kind = "supporting"  # => catalog helps the core but does not differentiate it

# => Proves the stated business rule is observable.
assert (
    # => Keeps this domain step explicit and reviewable.
    NotificationGateway().send("hello") == "sent:hello" and catalog_kind == "supporting"
    # => Keeps this domain step explicit and reviewable.
)
