"""Example 60: Refactor to State.

co-33 (refactor to pattern): a boolean-flag implementation of order lifecycle
(is_paid, is_shipped, is_cancelled -- independently settable) is refactored to the
State pattern -- co-29 (state): each lifecycle stage becomes its own class, and the
current-state object is the only thing that decides which transitions are legal,
making invalid flag combinations unrepresentable.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

# ============================================================
# BEFORE: boolean-flag soup -- nothing prevents illegal combinations
# ============================================================


class FlagOrder:  # => the original, unrefactored order
    def __init__(self) -> None:  # => sets up all three independent boolean flags below
        self.is_paid = False  # => three independent booleans...
        self.is_shipped = False  # => ...that can be set in ANY combination...
        self.is_cancelled = False  # => ...including ones that make no business sense

    def mark_shipped(self) -> None:  # => nothing here checks is_paid first
        self.is_shipped = True  # => BUG: this can fire even when is_paid is still False
        # => nothing in FlagOrder's design stops mark_shipped() from running before is_paid is ever set


# ============================================================
# AFTER: the State pattern -- illegal transitions are structurally impossible
# ============================================================


class OrderState(ABC):  # => the shared interface every concrete state implements
    @abstractmethod  # => forces every concrete state to define its own pay() behavior
    def pay(self, order: "StateOrder") -> None:  # => only states where paying is legal override this meaningfully
        raise NotImplementedError  # => abstract method body, never actually executed

    @abstractmethod  # => forces every concrete state to define its own ship() behavior
    def ship(self, order: "StateOrder") -> None:  # => only the Paid state allows shipping
        raise NotImplementedError  # => abstract method body, never actually executed

    def name(self) -> str:  # => a readable label for the current state, used in tests and printing
        return type(self).__name__  # => e.g. "Created", "Paid", "Shipped"


class Created(OrderState):  # => the starting state: nothing has happened yet
    def pay(self, order: "StateOrder") -> None:  # => the ONLY legal transition out of Created
        order.state = Paid()  # => moves the order into the Paid state

    def ship(self, order: "StateOrder") -> None:  # => shipping from Created is illegal
        raise ValueError("cannot ship an order that has not been paid")  # => structurally rejected, not just unwise


# => Paid is reachable only via Created.pay() above -- there is no way to construct an order that skips it
class Paid(OrderState):  # => after payment, before shipping
    def pay(self, order: "StateOrder") -> None:  # => paying twice is illegal
        raise ValueError("order is already paid")  # => Paid has no legal pay() transition

    def ship(self, order: "StateOrder") -> None:  # => the ONLY legal transition out of Paid
        order.state = Shipped()  # => moves the order into the Shipped state


# => Shipped is the terminal state: both its methods only ever raise, matching a real "closed" order
class Shipped(OrderState):  # => the terminal happy-path state
    def pay(self, order: "StateOrder") -> None:  # => paying a shipped order is illegal
        raise ValueError("order is already shipped")  # => Shipped has no legal pay() transition

    def ship(self, order: "StateOrder") -> None:  # => shipping twice is illegal
        raise ValueError("order is already shipped")  # => Shipped has no legal ship() transition


# => StateOrder itself contains ZERO business rules -- every legality check lives inside the state classes above
class StateOrder:  # => the refactored order -- delegates every transition to its current state object
    def __init__(self) -> None:  # => starts every new order in a single, well-defined state
        self.state: OrderState = Created()  # => starts in the Created state, same as FlagOrder's initial flags

    def pay(self) -> None:  # => delegates to whichever state object is current
        self.state.pay(self)  # => the STATE decides whether this is legal, not an if-chain here

    def ship(self) -> None:  # => delegates to whichever state object is current
        self.state.ship(self)  # => "shipped without paid" cannot happen: Created.ship() always raises


if __name__ == "__main__":  # => demonstration entry point, executed only when this file is run directly
    flag_order = FlagOrder()  # => the old version
    flag_order.mark_shipped()  # => BUG reproduced: shipped is True even though paid is still False
    print(flag_order.is_shipped, flag_order.is_paid)  # => demonstrates the illegal combination the flags allow
    # => Output: True False

    state_order = StateOrder()  # => the refactored version
    try:  # => wraps the illegal transition attempt so its ValueError can be shown
        state_order.ship()  # => attempting the same illegal move
    except ValueError as exc:  # => catches the rejection raised by Created.ship()
        print(exc)  # => the State pattern rejects it outright
    # => Output: cannot ship an order that has not been paid

    state_order.pay()  # => legal: Created -> Paid
    state_order.ship()  # => legal: Paid -> Shipped
    print(state_order.state.name())  # => confirms the final state
    # => Output: Shipped
