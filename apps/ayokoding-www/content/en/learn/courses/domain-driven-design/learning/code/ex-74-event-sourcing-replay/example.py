# => Keeps this domain step explicit and reviewable.
"""Example 74: replay folds an event stream into current state."""

events = ["OrderPlaced", "OrderPaid"]  # => recorded facts are the source of truth


# => Names policy so callers do not recreate the rule.
def replay(stream: list[str]) -> str:
    state = "draft"  # => start from the neutral state
    # => Applies the policy consistently to each value.
    for event in stream:
        # => Keeps scenario data close to the rule it exercises.
        state = {"OrderPlaced": "placed", "OrderPaid": "paid"}[
            # => Keeps this domain step explicit and reviewable.
            event
        ]  # => apply each fact
    # => Returns the domain result instead of leaking representation.
    return state


# => Proves the stated business rule is observable.
assert replay(events) == "paid"
