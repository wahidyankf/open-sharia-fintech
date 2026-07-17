"""Example 80: Clean Design Preview -- Strategy + Factory + Observer + Decorator, Under SOLID.

co-02, co-25, co-16, co-26, co-21: a small order/pricing engine combining four
patterns cohesively -- Strategy (co-25) for pluggable pricing rules, a factory
function (co-16) for choosing the right strategy, Observer (co-26) for
order-placed events, and a Decorator (co-21) that adds logging around pricing
without editing PricingEngine's own source. The whole system extends (new
pricing rule, new listener) without editing any CLOSED class -- OCP (co-02) in
practice, previewing the shape of this topic's capstone.
"""

from __future__ import annotations  # => defers type-hint evaluation for the forward references used below

from typing import Protocol  # => Protocol declares each pattern's interface structurally, no explicit inheritance


# ============================================================
# Strategy (co-25) -- pluggable pricing rules
# ============================================================


class PricingStrategy(Protocol):  # => the Strategy interface -- every pricing rule implements this
    def price(self, subtotal: float) -> float: ...  # => the ONE method every pricing rule must provide


class StandardPricing:  # => variant 1: no discount
    def price(self, subtotal: float) -> float:  # => satisfies PricingStrategy structurally
        return subtotal  # => the baseline, no discount applied


class MemberDiscountPricing:  # => variant 2: a member-only discount
    def price(self, subtotal: float) -> float:  # => satisfies PricingStrategy structurally
        return subtotal * 0.85  # => a flat 15% off for members


# ============================================================
# Factory (co-16) -- centralizes which strategy applies, so callers never branch on membership
# ============================================================


def make_pricing_strategy(is_member: bool) -> PricingStrategy:  # => co-16: a factory function, not a class switch
    return MemberDiscountPricing() if is_member else StandardPricing()  # => the ONE place membership is decided


# ============================================================
# Observer (co-26) -- order-placed events, decoupled from the pricing engine itself
# ============================================================


class OrderListener(Protocol):  # => the Observer interface -- every listener implements this
    def on_order_placed(self, total: float) -> None: ...  # => the ONE callback every listener must provide


class ReceiptPrinter:  # => a concrete listener -- the engine never imports this class by name
    def __init__(self) -> None:  # => the constructor
        self.receipts: list[str] = []  # => this listener's own log, populated only by on_order_placed

    def on_order_placed(self, total: float) -> None:  # => satisfies OrderListener structurally
        self.receipts.append(f"receipt: ${total:.2f}")  # => this listener's OWN reaction to the event


class PricingEngine:  # => co-02: CLOSED for modification -- new listeners/strategies never require editing this
    def __init__(self) -> None:  # => the constructor
        self._listeners: list[OrderListener] = []  # => an OPEN list of observers, populated via add_listener()

    def add_listener(self, listener: OrderListener) -> None:  # => co-26: any listener can be registered, unnamed here
        self._listeners.append(listener)  # => the engine never knows or cares WHAT the listener does

    def place_order(self, subtotal: float, strategy: PricingStrategy) -> float:  # => the ONE orchestrating method
        total = strategy.price(subtotal)  # => co-25: delegates the varying part to the strategy
        for listener in self._listeners:  # => co-26: notifies every registered observer, none hard-coded
            listener.on_order_placed(total)  # => each listener reacts independently, engine stays ignorant of how
        return total  # => hands the computed total back to the caller


# ============================================================
# Decorator (co-21) -- wraps the engine with logging, no edits inside PricingEngine
# ============================================================


class LoggingPricingEngine:  # => co-21: adds cross-cutting logging around the CLOSED PricingEngine
    def __init__(self, wrapped: PricingEngine) -> None:  # => the constructor
        self._wrapped = wrapped  # => the CLOSED engine being decorated, held as a collaborator
        self.log: list[float] = []  # => the cross-cutting log this decorator adds

    def add_listener(self, listener: OrderListener) -> None:  # => forwards to the wrapped engine, same interface
        self._wrapped.add_listener(listener)  # => delegates -- the decorator adds no new listener behavior here

    def place_order(self, subtotal: float, strategy: PricingStrategy) -> float:  # => forwards, then logs
        total = self._wrapped.place_order(subtotal, strategy)  # => delegates the REAL work to the wrapped engine
        self.log.append(total)  # => logging bolted on from OUTSIDE -- PricingEngine's source untouched
        return total  # => the SAME result the wrapped engine would have returned


if __name__ == "__main__":  # => demonstration entry point, executed only when this file is run directly
    engine = LoggingPricingEngine(PricingEngine())  # => the CLOSED engine, wrapped in logging from the outside
    receipts = ReceiptPrinter()  # => a concrete observer, unknown to PricingEngine by name
    engine.add_listener(receipts)  # => registers the observer through the decorator, which forwards it

    total_standard = engine.place_order(100.0, make_pricing_strategy(is_member=False))  # => strategy 1, via the factory
    print(total_standard)  # => confirms the standard pricing rule ran, unmodified
    # => Output: 100.0

    total_member = engine.place_order(100.0, make_pricing_strategy(is_member=True))  # => strategy 2, via the factory
    print(total_member)  # => confirms the member discount rule ran, unmodified
    # => Output: 85.0

    print(receipts.receipts)  # => confirms the observer reacted to BOTH order-placed events
    # => Output: ['receipt: $100.00', 'receipt: $85.00']

    print(engine.log)  # => the decorator logged both totals without PricingEngine knowing it was wrapped
    # => Output: [100.0, 85.0]
