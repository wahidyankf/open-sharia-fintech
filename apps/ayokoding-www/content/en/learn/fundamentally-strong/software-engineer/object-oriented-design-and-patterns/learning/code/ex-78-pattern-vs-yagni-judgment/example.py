"""Example 78: Pattern-or-Not -- A YAGNI Judgment Call, Across Three Scenarios.

co-34, co-02: patterns are not free -- each one adds indirection that must earn
its keep. Three scenarios, three different verdicts, each justified by a
concrete signal (not a hunch): how many variations exist TODAY, and how likely
a second one really is.
"""

from __future__ import annotations  # => defers type-hint evaluation, used only by Scenario 2's Protocol

from typing import Protocol  # => Protocol declares DiscountStrategy -- used ONLY where the pattern is justified

# ============================================================
# Scenario 1: ONE email formatter, no second implementation planned -- SKIP the pattern
# ============================================================


def format_welcome_email(username: str) -> str:  # => a PLAIN function -- no Strategy interface, no factory
    # => Judgment: only one email format exists, and the product has no roadmap item for a second one.
    # => Wrapping this in a Strategy pattern today buys zero flexibility and adds one more class to navigate.
    return f"Welcome, {username}!"  # => the entire behavior, in one line -- no interface needed to swap it later


# ============================================================
# Scenario 2: THREE discount rules today, a fourth confirmed on the roadmap -- USE Strategy
# ============================================================


class DiscountStrategy(Protocol):  # => co-25: justified here -- 3 variants exist NOW, a 4th is already planned
    def apply(self, subtotal: float) -> float: ...  # => the ONE method every discount rule must provide


class NoDiscount:  # => variant 1 of 3, already real today
    def apply(self, subtotal: float) -> float:  # => satisfies DiscountStrategy structurally
        return subtotal  # => no discount at all


class TenPercentOff:  # => variant 2 of 3, already real today
    def apply(self, subtotal: float) -> float:  # => satisfies DiscountStrategy structurally
        return subtotal * 0.90  # => a flat 10% off


class BuyOneGetOneFree:  # => variant 3 of 3, already real today
    def apply(self, subtotal: float) -> float:  # => satisfies DiscountStrategy structurally
        return subtotal * 0.50  # => an effective 50% off


def checkout_total(subtotal: float, discount: DiscountStrategy) -> float:  # => the ONE dispatcher, edited zero times
    # => Judgment: THREE real variants exist today (not hypothetical), and a fourth is already on the
    # => roadmap. The indirection pays for itself immediately, not speculatively.
    return discount.apply(subtotal)  # => delegates the VARYING part to whichever strategy was passed in


# ============================================================
# Scenario 3: ONE-OFF internal report converter, used once, thrown away after -- SKIP the pattern
# ============================================================


def convert_report_to_csv_line(fields: list[str]) -> str:  # => a PLAIN function -- no Converter interface
    # => Judgment: this runs once, for one internal report, with a known lifetime of a single script run.
    # => A pluggable Converter interface here is premature abstraction (ex-66) wearing a different hat.
    return ",".join(fields)  # => the entire behavior, in one line -- no interface needed for a one-off script


if __name__ == "__main__":  # => demonstration entry point, executed only when this file is run directly
    print(format_welcome_email("Ada"))  # => scenario 1: a plain function, no pattern applied
    # => Output: Welcome, Ada!

    print(checkout_total(100.0, BuyOneGetOneFree()))  # => scenario 2: Strategy, justified by 3+ real variants
    # => Output: 50.0

    print(convert_report_to_csv_line(["2026-07-17", "42", "ok"]))  # => scenario 3: a plain function, no pattern applied
    # => Output: 2026-07-17,42,ok
