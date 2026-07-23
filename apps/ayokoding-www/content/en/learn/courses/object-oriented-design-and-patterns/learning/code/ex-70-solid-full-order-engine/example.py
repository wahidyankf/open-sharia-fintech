"""Example 70: SOLID -- Full Order Engine.

co-01..co-05: all five SOLID principles applied together to one small order engine,
each at its own seam -- SRP splits pricing/persistence/receipts into three classes;
OCP adds a new discount without editing the dispatcher; LSP lets any DiscountStrategy
substitute for another without breaking OrderCalculator; ISP gives OrderService only
the narrow Repository protocol it needs, not a fat one; DIP has OrderService depend
on that protocol, not a concrete database class.
"""

from __future__ import annotations  # => defers type-hint evaluation for the forward references used below

from dataclasses import dataclass, field  # => field() supplies a safe mutable default for Order.items
from typing import Protocol  # => Protocol declares the DiscountStrategy and Repository abstractions

# ============================================================
# SRP -- three classes, three reasons to change
# ============================================================


@dataclass  # => generates __init__ from the field below
class Order:  # => plain data: an order's line items
    items: dict[str, float] = field(default_factory=dict)  # => item name -> unit price


class DiscountStrategy(Protocol):  # => OCP: new discounts are added as new classes, not new elif branches
    def apply(self, subtotal: float) -> float: ...  # => every strategy takes a subtotal, returns the discounted total


class NoDiscount:  # => LSP: substitutable for any other DiscountStrategy -- never breaks a caller's expectations
    def apply(self, subtotal: float) -> float:  # => satisfies DiscountStrategy structurally
        return subtotal  # => no discount applied


class TenPercentOff:  # => LSP: also substitutable -- honors the SAME contract (never returns MORE than subtotal)
    def apply(self, subtotal: float) -> float:  # => satisfies DiscountStrategy structurally
        return subtotal * 0.90  # => a flat 10% off, still honors the "never exceeds subtotal" contract


# => OrderCalculator never imports InMemoryRepository or ReceiptFormatter -- it only knows discount strategies
class OrderCalculator:  # => SRP: pricing, and only pricing -- depends on the DiscountStrategy ABSTRACTION (DIP)
    def total(self, order: Order, discount: DiscountStrategy) -> float:  # => OCP: adding a discount needs no edit here
        subtotal = sum(order.items.values())  # => information-expert: Order holds items, this sums them
        return discount.apply(subtotal)  # => delegates the VARYING part to whichever strategy was passed in


class Repository(Protocol):  # => ISP: OrderService depends on ONLY this narrow protocol, not a fat DB interface
    def save(self, order_id: str, total: float) -> None: ...  # => the ONE method OrderService actually calls


# => a real implementation might be Postgres or Redis -- OrderService would not need to change at all
class InMemoryRepository:  # => a concrete, swappable implementation of the Repository protocol
    def __init__(self) -> None:  # => the constructor
        self.saved: dict[str, float] = {}  # => order_id -> total, standing in for a real database

    def save(self, order_id: str, total: float) -> None:  # => satisfies Repository structurally
        self.saved[order_id] = total  # => the ONE narrow responsibility this class has


class ReceiptFormatter:  # => SRP: formatting, and only formatting -- its own reason to change, separate from pricing
    def format(self, order_id: str, total: float) -> str:  # => defines the format() method
        return f"Order {order_id}: ${total:.2f}"  # => a pure string-building step, no pricing or persistence here


# => this is the class DIP is really about: it depends on Repository (abstract), never on InMemoryRepository (concrete)
class OrderService:  # => DIP: depends on the Repository ABSTRACTION, never on InMemoryRepository directly
    def __init__(self, calculator: OrderCalculator, repository: Repository) -> None:  # => both injected, not constructed
        self._calculator = calculator  # => the high-level policy owns these abstractions
        self._repository = repository  # => held as a collaborator, never constructed internally

    def checkout(self, order_id: str, order: Order, discount: DiscountStrategy) -> float:  # => the ONE orchestrating method
        total = self._calculator.total(order, discount)  # => delegates pricing
        self._repository.save(order_id, total)  # => delegates persistence, via the ABSTRACT protocol only
        return total  # => hands the computed total back to the caller


if __name__ == "__main__":  # => demonstration entry point, executed only when this file is run directly
    order = Order(items={"Book": 20.0, "Pen": 5.0})  # => subtotal = 25.0
    calculator = OrderCalculator()  # => constructs the pricing collaborator
    repository = InMemoryRepository()  # => constructs the persistence collaborator
    service = OrderService(calculator, repository)  # => DIP: injected, not hard-coded

    total_no_discount = service.checkout("ord-1", order, NoDiscount())  # => LSP: NoDiscount substitutes cleanly
    print(total_no_discount)  # => the undiscounted subtotal
    # => Output: 25.0

    total_with_discount = service.checkout("ord-2", order, TenPercentOff())  # => OCP: swapped WITHOUT editing service
    print(total_with_discount)  # => the SAME checkout() method, a different discount object
    # => Output: 22.5

    formatter = ReceiptFormatter()  # => SRP: a third, independent responsibility
    print(formatter.format("ord-2", total_with_discount))  # => confirms formatting stays separate from pricing
    # => Output: Order ord-2: $22.50

    print(repository.saved)  # => confirms persistence happened via the Repository protocol only
    # => Output: {'ord-1': 25.0, 'ord-2': 22.5}
    # => all five SOLID seams cooperated in this one run: SRP, OCP, LSP, ISP, and DIP each did real work above
