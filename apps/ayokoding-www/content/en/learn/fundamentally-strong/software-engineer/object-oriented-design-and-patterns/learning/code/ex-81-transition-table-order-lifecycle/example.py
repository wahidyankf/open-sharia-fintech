"""Example 81: Transition-Table FSM -- Order Lifecycle.

co-35: an order lifecycle (created -> paid -> shipped -> delivered, with
cancellation from created or paid) modeled as an explicit
state x event -> state TRANSITION TABLE -- a plain dict, not a chain of `if`
statements. Every illegal event in a state is rejected by the TABLE ITSELF
(a missing key), so "what can happen next" is one data structure you can read
top to bottom, not logic scattered across methods.
"""

from __future__ import annotations  # => defers type-hint evaluation for the dict[tuple[str, str], str] alias below


class IllegalTransition(Exception):  # => raised when the table has no entry for (state, event)
    pass  # => a plain marker exception -- no extra fields needed, the message carries the detail


# ============================================================
# The transition table -- the ENTIRE lifecycle logic lives in this one dict
# ============================================================

# => co-35: this dict IS the state machine -- reading it top to bottom answers "what can happen next"
ORDER_TRANSITIONS: dict[tuple[str, str], str] = {  # => keys are (current_state, event) pairs, values are next states
    ("created", "pay"): "paid",  # => created -> paid, on the "pay" event
    ("created", "cancel"): "cancelled",  # => created -> cancelled, on the "cancel" event
    ("paid", "ship"): "shipped",  # => paid -> shipped, on the "ship" event
    ("paid", "cancel"): "cancelled",  # => paid -> cancelled, on the "cancel" event
    ("shipped", "deliver"): "delivered",  # => shipped -> delivered, on the "deliver" event
    # => no ("shipped", "cancel") entry -- a shipped order can no longer be cancelled, by OMISSION
    # => no ("delivered", *) entries -- delivered is terminal, by omission
    # => no ("cancelled", *) entries -- cancelled is terminal, by omission
}  # => closes the table -- every legal transition in the entire lifecycle is visible above, nothing hidden elsewhere


class OrderFsm:  # => a thin wrapper around the table -- holds no transition logic of its own
    def __init__(self) -> None:  # => the constructor
        self.state = "created"  # => every order starts in this one state

    def send(self, event: str) -> str:  # => the ONE method that ever changes self.state
        key = (self.state, event)  # => builds the (state, event) lookup key for the table
        if key not in ORDER_TRANSITIONS:  # => the TABLE rejects illegal events -- no scattered if-checks anywhere
            raise IllegalTransition(f"event {event!r} is illegal in state {self.state!r}")  # => an honest, specific failure
        self.state = ORDER_TRANSITIONS[key]  # => the table itself supplies the next state, no branching logic here
        return self.state  # => hands back the new state to the caller


if __name__ == "__main__":  # => demonstration entry point, executed only when this file is run directly
    order = OrderFsm()  # => starts in "created", per __init__
    print(order.send("pay"))  # => created -> paid, a table lookup
    # => Output: paid
    print(order.send("ship"))  # => paid -> shipped
    # => Output: shipped
    print(order.send("deliver"))  # => shipped -> delivered
    # => Output: delivered

    try:  # => attempts an event that the table has no entry for
        order.send("cancel")  # => illegal: delivered has no "cancel" entry in the table
    except IllegalTransition as error:  # => the table's own omission produced this, not a manual if-check
        print(error)  # => shows the honest, specific failure message
    # => Output: event 'cancel' is illegal in state 'delivered'
