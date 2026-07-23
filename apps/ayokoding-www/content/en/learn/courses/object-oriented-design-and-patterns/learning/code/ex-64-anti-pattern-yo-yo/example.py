"""Example 64: Anti-Pattern -- Yo-Yo Inheritance.

co-34 (anti-pattern recognition): yo-yo inheritance is diagnosed when understanding
one method call requires jumping up and down a deep hierarchy, following super()
calls back and forth across many classes. The fix is flattening: collapse the chain
to the minimum depth that still expresses a genuine is-a relationship.
"""

from __future__ import annotations

# ============================================================
# BEFORE: understanding discount() requires jumping through 4 classes
# ============================================================


class BasePricer:  # => level 1
    def discount(self, price: float) -> float:  # => defines the base case
        return price  # => no discount at this level


class RegionalPricer(BasePricer):  # => level 2 -- must jump UP to BasePricer to see the base case
    def discount(self, price: float) -> float:  # => override signature, unchanged from BasePricer's
        base = super().discount(price)  # => jump UP to level 1
        return base * 0.95  # => 5% regional discount, only visible by reading THIS override


class SeasonalPricer(RegionalPricer):  # => level 3 -- must jump UP through level 2 AND level 1
    def discount(self, price: float) -> float:  # => override signature, unchanged from the level below
        base = super().discount(price)  # => jump UP to level 2, which itself jumps UP to level 1
        return base * 0.90  # => additional 10% seasonal discount


class LoyaltyPricer(SeasonalPricer):  # => level 4 -- understanding this needs all THREE super() calls above it
    def discount(self, price: float) -> float:  # => override signature, unchanged from all three levels below
        base = super().discount(price)  # => jump UP to level 3, which jumps to level 2, which jumps to level 1
        return base * 0.98  # => additional 2% loyalty discount -- the "yo-yo": up, up, up just to see the total


# => this function literalizes "yo-yo" as a number: how many classes must be opened to read one method fully
def count_hops_to_understand(cls: type, method_name: str) -> int:  # => a mechanical yo-yo detector
    hops = 0  # => counts how many classes in the MRO define this method
    for klass in cls.__mro__:  # => walk the method resolution order top to bottom
        if method_name in klass.__dict__:  # => this class DEFINES (not just inherits) the method
            hops += 1  # => reading the full behavior requires visiting this class too
    return hops  # => 4+ hops for one method is the yo-yo smell


# ============================================================
# AFTER: flattened to depth 1 -- discount is one function, fully readable in place
# ============================================================


def flattened_discount(price: float) -> float:  # => the SAME final formula, with zero jumps required to read it
    return price * 0.95 * 0.90 * 0.98  # => regional * seasonal * loyalty, all visible on one line


if __name__ == "__main__":  # => demonstration entry point, executed only when this file is run directly
    print(count_hops_to_understand(LoyaltyPricer, "discount"))  # => 4 classes must be read to understand ONE method
    # => Output: 4
    loyalty = LoyaltyPricer()  # => instantiating the deepest, most yo-yo-prone class
    print(round(loyalty.discount(100.0), 4))  # => the yo-yo version's result
    # => Output: 83.79
    print(round(flattened_discount(100.0), 4))  # => the flattened version's result -- identical, zero jumps
    # => Output: 83.79
