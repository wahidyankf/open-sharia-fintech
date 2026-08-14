"""Example 74: replay folds an event stream into current state."""

events = ["OrderPlaced", "OrderPaid"]  # => recorded facts are the source of truth


def replay(stream: list[str]) -> str:
    state = "draft"  # => start from the neutral state
    for event in stream:
        state = {"OrderPlaced": "placed", "OrderPaid": "paid"}[
            event
        ]  # => apply each fact
    return state


assert replay(events) == "paid"
