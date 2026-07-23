"""Example 84: Transition-Table FSM vs. Boolean-Flag Soup -- a Direct Contrast.

co-35, co-33: places the transition-table FSM (ex-81) side by side with the
boolean-flag order (ex-60's `FlagOrder`, reproduced here for a self-contained
comparison). The flag version can represent `is_shipped=True, is_paid=False`
-- a combination the business rules say should be impossible. The FSM version
CANNOT represent this: "shipped" is a single string value, and there is no
combination of table entries that reaches it without first passing through
"paid". The illegal combination is unrepresentable, not just unreached.
"""

from __future__ import annotations  # => defers type-hint evaluation for the dict[tuple[str, str], str] alias below


class IllegalTransition(Exception):  # => raised when the FSM table has no entry for (state, event)
    pass  # => a plain marker exception -- no extra fields needed, the message carries the detail


# ============================================================
# BEFORE: boolean-flag soup -- co-33's starting point, reproduced for comparison
# ============================================================


class FlagOrder:  # => three independent booleans -- 2**3 = 8 representable combinations
    def __init__(self) -> None:  # => the constructor
        self.is_paid = False  # => independent flag 1 of 3 -- nothing ties this to the other two
        self.is_shipped = False  # => independent flag 2 of 3 -- settable regardless of is_paid
        self.is_cancelled = False  # => independent flag 3 of 3 -- settable regardless of the other two


# ============================================================
# AFTER: the transition-table FSM (ex-81) -- one string field, only reachable states exist
# ============================================================

# => co-35: contrast with FlagOrder above -- ONE field (state), not three independent booleans
ORDER_TRANSITIONS: dict[tuple[str, str], str] = {  # => keys are (state, event), values are the next state
    ("created", "pay"): "paid",  # => created -> paid, on the "pay" event
    ("created", "cancel"): "cancelled",  # => created -> cancelled, on the "cancel" event
    ("paid", "ship"): "shipped",  # => paid -> shipped -- only reachable AFTER "paid"
    ("paid", "cancel"): "cancelled",  # => paid -> cancelled, on the "cancel" event
    ("shipped", "deliver"): "delivered",  # => shipped -> delivered, on the "deliver" event
}  # => closes the table -- "shipped" only ever appears as a value reached THROUGH "paid", never around it


class OrderFsm:  # => a single string field -- only states REACHABLE by walking the table can ever exist
    def __init__(self) -> None:  # => the constructor
        self.state = "created"  # => the ONE field this class has -- no independent booleans to fall out of sync

    def send(self, event: str) -> str:  # => the ONE method that ever changes self.state
        key = (self.state, event)  # => builds the (state, event) lookup key for the table
        if key not in ORDER_TRANSITIONS:  # => the TABLE rejects illegal events -- no scattered if-checks anywhere
            raise IllegalTransition(f"event {event!r} is illegal in state {self.state!r}")  # => an honest, specific failure
        self.state = ORDER_TRANSITIONS[key]  # => the table itself supplies the next state, no branching logic here
        return self.state  # => hands back the new state to the caller


def count_representable_flag_combinations() -> int:  # => 3 booleans-worth of independence -> 2**3 combos, ALL settable
    return 2 * 2 * 2  # => is_paid x is_shipped x is_cancelled, each independently True/False


# => co-33: the gap between these two counts IS the illegal-state surface that boolean flags leave open
def count_reachable_fsm_states() -> int:  # => only the states that appear as a VALUE in the transition table
    reachable = {"created"} | set(ORDER_TRANSITIONS.values())  # => created is the start; the rest come from the table
    return len(reachable)  # => a strictly smaller number than the flag version's combinations, by construction


if __name__ == "__main__":  # => demonstration entry point, executed only when this file is run directly
    flags = FlagOrder()  # => starts with all three flags False
    flags.is_shipped = True  # => nothing in the FlagOrder class prevents setting this WITHOUT is_paid
    print(flags.is_shipped, flags.is_paid)  # => the illegal combination IS representable -- it just happened
    # => Output: True False

    fsm = OrderFsm()  # => starts in "created", the FSM's single field
    try:  # => attempts the FSM equivalent of the same illegal combination above
        fsm.send("ship")  # => the FSM equivalent of "become shipped without paying first"
    except IllegalTransition as error:  # => the table's own omission produced this, not a manual if-check
        print(error)  # => structurally rejected: there is no table entry for ("created", "ship")
    # => Output: event 'ship' is illegal in state 'created'

    print(count_representable_flag_combinations())  # => 8 combinations the type system allows
    # => Output: 8
    print(count_reachable_fsm_states())  # => only 5 states are reachable at all -- illegal combos don't exist as values
    # => Output: 5
