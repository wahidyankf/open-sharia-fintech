# => Keeps this domain step explicit and reviewable.
"""Example 46: a dispatcher sends facts to subscribed handlers."""

seen: list[str] = []  # => handler side effects are observable in a local test double


# => Names policy so callers do not recreate the rule.
def handle(event: str) -> None:
    seen.append(event)  # => subscriber reacts without changing the producer


# => Names policy so callers do not recreate the rule.
def publish(event: str, handlers: list[object]) -> None:
    # => Applies the policy consistently to each value.
    for handler in handlers:
        handler(event)  # type: ignore[operator]  # => dispatch each subscriber


# => Keeps this domain step explicit and reviewable.
publish("OrderPlaced", [handle])
# => Proves the stated business rule is observable.
assert seen == ["OrderPlaced"]
