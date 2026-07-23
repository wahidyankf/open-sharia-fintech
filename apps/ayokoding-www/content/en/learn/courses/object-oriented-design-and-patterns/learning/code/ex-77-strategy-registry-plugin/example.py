"""Example 77: Strategy -- Registry-Driven Plugin System.

co-25, co-02: a `PricingStrategyRegistry` maps a string key to a
`PricingStrategy`. Core code (`checkout`) only ever looks a strategy up by
name -- it never imports a concrete strategy class. A THIRD-PARTY strategy
registers itself into the SAME registry from outside the core module and
`checkout` picks it up with zero edits to core code, satisfying OCP (co-02)
through Strategy (co-25).
"""

from __future__ import annotations  # => defers type-hint evaluation for the forward references used below

from typing import Protocol  # => Protocol declares the Strategy shape every pricing rule must satisfy


class PricingStrategy(Protocol):  # => the Strategy interface -- every pricing rule implements this
    def price(self, subtotal: float) -> float: ...  # => the ONE method every pricing rule must provide


# => this dict IS the plugin seam: any code, core or third-party, can call register() at any time
class PricingStrategyRegistry:  # => the plugin mechanism: a name -> strategy lookup, owned by core code
    def __init__(self) -> None:  # => the constructor
        self._strategies: dict[str, PricingStrategy] = {}  # => empty at construction, filled by register() calls

    def register(self, name: str, strategy: PricingStrategy) -> None:  # => any caller, core or third-party, can add
        self._strategies[name] = strategy  # => stores under the string key -- no import required by the registry

    def get(self, name: str) -> PricingStrategy:  # => looks up by NAME, never by class
        if name not in self._strategies:  # => an honest, explicit check before the lookup
            raise KeyError(f"no pricing strategy registered under {name!r}")  # => an honest failure for unknown names
        return self._strategies[name]  # => hands back whichever strategy was registered under this name


# ============================================================
# CORE -- ships with one built-in strategy; never imports anything third-party
# ============================================================


class StandardPricing:  # => a built-in, core strategy
    def price(self, subtotal: float) -> float:  # => satisfies PricingStrategy structurally
        return subtotal  # => no discount at all -- the baseline


def checkout(registry: PricingStrategyRegistry, strategy_name: str, subtotal: float) -> float:  # => core's ONE entry point
    strategy = registry.get(strategy_name)  # => core code looks up BY NAME -- no concrete strategy import here
    return strategy.price(subtotal)  # => delegates the VARYING part entirely to whichever strategy was found


# ============================================================
# THIRD-PARTY PLUGIN -- registers into the SAME registry, defined entirely outside core
# ============================================================


# => this class could live in an entirely separate package -- checkout() never imports it by name
class BlackFridayPricing:  # => a plugin author's OWN class -- core never imports this
    def price(self, subtotal: float) -> float:  # => satisfies PricingStrategy structurally, same shape as core's
        return subtotal * 0.60  # => an aggressive 40% off, defined entirely outside core


if __name__ == "__main__":  # => demonstration entry point, executed only when this file is run directly
    registry = PricingStrategyRegistry()  # => the single shared registry both core and the plugin use
    registry.register("standard", StandardPricing())  # => core registers its own built-in strategy

    print(checkout(registry, "standard", 100.0))  # => resolves "standard" through the registry, not an import
    # => Output: 100.0

    registry.register("black-friday", BlackFridayPricing())  # => THIRD PARTY plugs in -- zero edits to checkout()
    print(checkout(registry, "black-friday", 100.0))  # => the SAME checkout() function, a brand-new strategy name
    # => Output: 60.0
