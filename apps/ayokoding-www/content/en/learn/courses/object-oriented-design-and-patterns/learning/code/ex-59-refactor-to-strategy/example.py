"""Example 59: Refactor to Strategy.

co-33 (refactor to pattern): an embedded if-chain computing shipping cost by method
name is refactored to a strategy family under a locking test suite that stays green
through every step -- co-25 (strategy): each shipping method becomes its own small
callable, and the dispatcher looks the method up instead of branching on it.
"""

from __future__ import annotations

from typing import Callable

# ============================================================
# BEFORE: an if-chain that must be edited for every new shipping method
# ============================================================


def shipping_cost_if_chain(method: str, weight_kg: float) -> float:  # => the original, unrefactored dispatcher
    if method == "standard":  # => branch 1: flat rate per kg
        return 2.0 * weight_kg  # => $2/kg
    elif method == "express":  # => branch 2: higher flat rate
        return 5.0 * weight_kg  # => $5/kg
    elif method == "overnight":  # => branch 3: highest flat rate plus a surcharge
        return 10.0 * weight_kg + 15.0  # => $10/kg plus a $15 fixed surcharge
    raise ValueError(f"unknown shipping method: {method}")  # => every new method needs a new elif here (OCP violation)


# ============================================================
# AFTER: a strategy family -- new methods are added, not edited into a switch
# ============================================================

ShippingStrategy = Callable[[float], float]  # => a strategy is just "weight_kg -> cost", nothing more


def standard_shipping(weight_kg: float) -> float:  # => strategy 1, extracted verbatim from the if-chain
    return 2.0 * weight_kg  # => identical formula to the "standard" branch above


def express_shipping(weight_kg: float) -> float:  # => strategy 2, extracted verbatim
    return 5.0 * weight_kg  # => identical formula to the "express" branch above


def overnight_shipping(weight_kg: float) -> float:  # => strategy 3, extracted verbatim
    return 10.0 * weight_kg + 15.0  # => identical formula to the "overnight" branch above


# => three strategies extracted so far, each a pure one-line function with the exact old formula
SHIPPING_STRATEGIES: dict[str, ShippingStrategy] = {  # => the dispatch table replaces the if-chain entirely
    "standard": standard_shipping,  # => maps the method name to its strategy function
    "express": express_shipping,  # => maps a second method name to its strategy function
    "overnight": overnight_shipping,  # => maps a third method name to its strategy function
}  # => closes the dispatch table literal


def shipping_cost_via_strategy(method: str, weight_kg: float) -> float:  # => the refactored dispatcher
    strategy = SHIPPING_STRATEGIES.get(method)  # => look up the strategy by name, no branching required
    if strategy is None:  # => guard: unknown method still raises, matching the old behavior
        raise ValueError(f"unknown shipping method: {method}")  # => identical error message to the if-chain version
    return strategy(weight_kg)  # => delegate to whichever strategy was found


# => this is the OCP payoff: shipping_cost_via_strategy above needs zero edits to support this new method
def bulk_shipping(weight_kg: float) -> float:  # => a FOURTH method, added with zero edits to the dispatcher above
    return 1.0 * weight_kg - 3.0  # => cheapest rate, bulk discount baked in


if __name__ == "__main__":  # => demonstration entry point, executed only when this file is run directly
    print(shipping_cost_if_chain("express", 4.0))  # => old dispatcher, exercised for comparison
    # => Output: 20.0
    print(shipping_cost_via_strategy("express", 4.0))  # => new dispatcher, identical result
    # => Output: 20.0
    SHIPPING_STRATEGIES["bulk"] = bulk_shipping  # => adding "bulk" required zero edits to shipping_cost_via_strategy
    print(shipping_cost_via_strategy("bulk", 10.0))  # => the newly registered strategy works immediately
    # => Output: 7.0
