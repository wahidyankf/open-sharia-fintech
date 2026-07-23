"""Example 71: GRASP -- Full Assignment.

co-06..co-14: all nine GRASP patterns assigned across one small library-checkout
domain -- information expert, creator, controller, low coupling, high cohesion,
polymorphism, pure fabrication, indirection, and protected variations -- each
pattern placed at the point in the domain that motivated it.
"""

from __future__ import annotations  # => defers type-hint evaluation for the forward references used below

from dataclasses import dataclass  # => Loan uses only plain fields, so only dataclass itself is needed here
from datetime import date, timedelta  # => date drives due_date/overdue math, timedelta computes the loan period
from typing import Callable, Protocol  # => Protocol declares FeePolicy and OverdueNotifier, both stable seams

# ============================================================
# 9. Protected Variations -- an unstable fee RULE wrapped behind a stable interface
# ============================================================


class FeePolicy(Protocol):  # => the stable interface -- a fee-rule change never touches Loan
    def daily_rate(self) -> float: ...  # => the ONE method every fee rule must provide


class StandardFeePolicy:  # => one concrete, swappable rule
    def daily_rate(self) -> float:  # => satisfies FeePolicy structurally
        return 0.25  # => the standard-member daily rate


# ============================================================
# 6. Polymorphism -- dispatch on fee policy type, no if/elif type-switch anywhere
# ============================================================


class PremiumFeePolicy:  # => a SECOND concrete rule -- Loan never branches on which one it got
    def daily_rate(self) -> float:  # => satisfies FeePolicy structurally, same shape as StandardFeePolicy
        return 0.10  # => premium members pay a lower daily rate


# ============================================================
# 5. High Cohesion + 1. Information Expert -- Loan's methods all use ITS OWN fields
# ============================================================


@dataclass  # => generates __init__ from the fields below
class Loan:  # => holds due_date, so Loan is the natural INFORMATION EXPERT for lateness/fee math
    book_title: str  # => plain field, part of the generated __init__
    borrower: str  # => plain field, part of the generated __init__
    due_date: date  # => plain field, part of the generated __init__
    fee_policy: FeePolicy  # => co-14: depends on the STABLE interface, not a concrete policy class

    def days_overdue(self, today: date) -> int:  # => every method here reads ONLY this instance's own fields
        return max(0, (today - self.due_date).days)  # => high cohesion: no unrelated state touched

    def fee(self, today: date) -> float:  # => information-expert: Loan owns due_date, so Loan computes the fee
        return self.days_overdue(today) * self.fee_policy.daily_rate()  # => co-6: dispatches polymorphically


# ============================================================
# 8. Pure Fabrication -- LoanRepository is not a domain concept, invented for persistence
# ============================================================


class LoanRepository:  # => co-12: a non-domain class that exists purely to keep Library IO-free
    def __init__(self) -> None:  # => the constructor
        self._loans: list[Loan] = []  # => stands in for a real database table

    def add(self, loan: Loan) -> None:  # => the ONE write path
        self._loans.append(loan)  # => appended, never mutated after this

    def all(self) -> list[Loan]:  # => the ONE read path
        return list(self._loans)  # => returns a COPY, so callers cannot mutate internal state


# ============================================================
# 2. Creator -- Library aggregates Loans, so Library is the natural creator of one
# ============================================================


class OverdueNotifier(Protocol):  # => co-13: the mediator's narrow interface
    def __call__(self, loan: Loan, /) -> None: ...  # => positional-only so a bare Callable[[Loan], None] matches structurally


class Library:  # => co-9: LOW COUPLING -- Library never imports a concrete notification class
    def __init__(self, repository: LoanRepository, on_overdue: OverdueNotifier | None = None) -> None:  # => both injected
        self._repository = repository  # => co-12: depends on the pure fabrication, not raw persistence code
        self._on_overdue: list[OverdueNotifier] = []  # => co-13: INDIRECTION -- a list of callbacks, not direct refs
        if on_overdue is not None:  # => the optional notifier is registered only if the caller supplied one
            self._on_overdue.append(on_overdue)  # => co-9: coupling is through a callable, not a concrete class

    def checkout(self, book_title: str, borrower: str, fee_policy: FeePolicy) -> Loan:  # => co-7: CREATOR
        due_date = date.today() + timedelta(days=14)  # => Library aggregates Loans, so it creates them (co-7)
        loan = Loan(book_title, borrower, due_date, fee_policy)  # => the natural creation point
        self._repository.add(loan)  # => delegated to the pure fabrication
        return loan  # => hands the newly created Loan back to the caller

    def check_for_overdue(self, today: date) -> list[Loan]:  # => scans every stored loan for lateness
        overdue = [loan for loan in self._repository.all() if loan.days_overdue(today) > 0]  # => filters via Loan itself
        for loan in overdue:  # => visits each overdue loan
            for notify in self._on_overdue:  # => co-13: Library talks only to the MEDIATOR list, never to a concrete notifier
                notify(loan)  # => co-9: no import of any concrete notification class anywhere in Library
        return overdue  # => hands the overdue subset back to the caller


# ============================================================
# 4. Controller -- routes the "checkout" event; the UI never touches Library directly
# ============================================================


class LibraryController:  # => co-8: a dedicated coordinating object between UI events and the domain
    def __init__(self, library: Library) -> None:  # => the constructor
        self._library = library  # => the ONE domain collaborator the controller coordinates with

    def handle_checkout_request(self, book_title: str, borrower: str, is_premium: bool) -> Loan:  # => the ENTRY POINT
        policy: FeePolicy = PremiumFeePolicy() if is_premium else StandardFeePolicy()  # => co-6: chosen, not switched on later
        return self._library.checkout(book_title, borrower, policy)  # => the UI calls THIS, never Library directly


# ============================================================
# Wiring: an event log stands in for a real NotificationService, decoupled via co-13
# ============================================================


def make_logging_notifier(log: list[str]) -> Callable[[Loan], None]:  # => co-9: Library only knows this is callable
    def notify(loan: Loan) -> None:  # => the actual callback, closing over `log`
        log.append(f"{loan.borrower} is overdue on {loan.book_title}")  # => the ONE side effect this notifier has

    return notify  # => a plain function IS a valid OverdueNotifier -- no class required


if __name__ == "__main__":  # => demonstration entry point, executed only when this file is run directly
    notifications: list[str] = []  # => the log the notifier closure above appends into
    repository = LoanRepository()  # => 8. pure fabrication
    library = Library(repository, on_overdue=make_logging_notifier(notifications))  # => 9. low coupling + 13 indirection
    controller = LibraryController(library)  # => 4. controller

    controller.handle_checkout_request("Clean Code", "Ada", is_premium=False)  # => 2. creator, via Library.checkout
    controller.handle_checkout_request("Refactoring", "Grace", is_premium=True)  # => 6. polymorphism: different policy

    past_due = date.today() + timedelta(days=20)  # => simulate 6 days overdue
    overdue_loans = library.check_for_overdue(past_due)  # => triggers both the query and the mediated notification
    print(len(overdue_loans))  # => both loans are overdue by this date
    # => Output: 2
    print(round(overdue_loans[0].fee(past_due), 2))  # => 1. information expert: Loan computes its own fee
    # => Output: 1.5
    print(round(overdue_loans[1].fee(past_due), 2))  # => 6. polymorphism: premium's LOWER daily rate applied
    # => Output: 0.6
    print(len(notifications))  # => 13. indirection worked: notifier fired without Library knowing its concrete type
    # => Output: 2
