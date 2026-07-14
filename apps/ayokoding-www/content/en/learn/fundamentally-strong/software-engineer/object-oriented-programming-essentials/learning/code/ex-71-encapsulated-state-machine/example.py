"""Example 71: An Order Enforcing Legal Status Transitions."""


class Order:  # => begins the Order class body
    _LEGAL_NEXT: dict[
        str, set[str]
    ] = {  # => the whole state machine, declared in one place
        "pending": {
            "shipped",
            "cancelled",
        },  # => from pending, only shipped or cancelled are legal
        "shipped": {"delivered"},  # => from shipped, only delivered is legal
        "delivered": set(),  # => a terminal state -- no legal transitions out of it
        "cancelled": set(),  # => also terminal -- no legal transitions out of it
    }  # => closes the state-machine table

    def __init__(
        self,
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self.status: str = "pending"  # => every Order starts in the same initial state

    def transition_to(
        self, new_status: str
    ) -> None:  # => defines the transition_to() method
        allowed: set[str] = self._LEGAL_NEXT[
            self.status
        ]  # => looks up what THIS status permits
        if (
            new_status not in allowed
        ):  # => guards every transition, not just the "obvious" ones
            raise ValueError(
                f"cannot go from {self.status} to {new_status}"
            )  # => rejects it
        self.status = (
            new_status  # => only reached once the transition is confirmed legal
        )


order: Order = Order()  # => constructs order
order.transition_to("shipped")  # => pending -> shipped is legal
print(order.status)  # => confirms the legal transition actually took effect
# => Output: shipped
try:  # => the block below is expected to raise
    order.transition_to("pending")  # => shipped -> pending is NOT in the legal set
except ValueError as exc:  # => catches the ValueError raised above
    print(exc)  # => prints the exact rejection message
# => Output: cannot go from shipped to pending
# => `_LEGAL_NEXT` names every allowed transition in one table, and `transition_to` is the ONLY method that ever changes `status`
