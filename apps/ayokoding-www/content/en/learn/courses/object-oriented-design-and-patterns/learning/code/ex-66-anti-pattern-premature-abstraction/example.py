"""Example 66: Anti-Pattern -- Premature Abstraction.

co-34 (anti-pattern recognition) + co-02 (OCP, its counterpart): a Strategy family
built for a SINGLE implementation ("just in case" a second one shows up) is
speculative generality -- extra indirection paid for before any real variation
exists. The fix is removing the abstraction and calling the one implementation
directly; OCP earns its indirection only once a second variant is real (Example 3).
"""

from __future__ import annotations  # => defers type-hint evaluation, not required here but kept for consistency

from abc import ABC, abstractmethod  # => the tools used to build the abstraction this example argues against

# ============================================================
# BEFORE: a strategy interface for exactly ONE implementation
# ============================================================


class TaxStrategy(ABC):  # => an interface built for "future" tax strategies that do not exist yet
    @abstractmethod  # => forces every future strategy to implement calculate() -- but only one ever will
    def calculate(self, amount: float) -> float:  # => the one abstract method every strategy would implement
        # => this body is dead code: @abstractmethod already forbids instantiating TaxStrategy directly
        raise NotImplementedError  # => abstract method body, never actually executed


# => this is the ONLY class that will ever subclass TaxStrategy in this codebase's actual history
class FlatRateTaxStrategy(TaxStrategy):  # => the ONLY implementation that has ever existed
    def calculate(self, amount: float) -> float:  # => the ONLY override that has ever existed or is planned
        return amount * 0.08  # => flat 8% tax -- there is no second rule to switch between


# => the strategy parameter exists to support variation that has never materialized
def total_with_tax_premature(amount: float, strategy: TaxStrategy) -> float:  # => a parameter for a choice nobody makes
    return amount + strategy.calculate(amount)  # => every caller passes the SAME FlatRateTaxStrategy() instance


# ============================================================
# AFTER: the abstraction is removed -- one function, one formula
# ============================================================


# => AFTER: same behavior, but the interface, the concrete class, and the parameter are all simply gone
def total_with_tax_simple(amount: float) -> float:  # => no interface, no strategy parameter, no indirection
    return amount + amount * 0.08  # => the SAME formula, with zero ceremony around it


# => a crude proxy metric, but it makes the added ceremony countable rather than just a feeling
def count_lines_of_indirection(strategy_based: bool) -> int:  # => a simple proxy for "how much ceremony"
    if strategy_based:  # => the premature-abstraction version needs: ABC + abstractmethod + concrete class + param
        return 4  # => TaxStrategy class, calculate() signature, FlatRateTaxStrategy class, strategy parameter
    return 0  # => the simplified version needs none of that
    # => the count itself never varies at runtime -- it exists only to make "more ceremony" a checkable fact


if __name__ == "__main__":  # => demonstration entry point, executed only when this file is run directly
    # => both branches below compute the exact same tax on the exact same amount -- only the ceremony differs
    premature = total_with_tax_premature(100.0, FlatRateTaxStrategy())  # => must construct a strategy just to call this
    print(premature)  # => the abstraction adds ceremony without adding any actual flexibility used anywhere
    # => Output: 108.0
    simple = total_with_tax_simple(100.0)  # => identical result, zero ceremony
    print(simple)  # => same number, arrived at directly
    # => Output: 108.0
    print(count_lines_of_indirection(strategy_based=True) > count_lines_of_indirection(strategy_based=False))  # => confirms the abstraction costs strictly more ceremony
    # => Output: True
