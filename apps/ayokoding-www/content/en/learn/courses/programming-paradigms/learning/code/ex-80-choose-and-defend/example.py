"""Example 80: Choose and Defend."""

from collections.abc import Mapping  # => the covariant read-only view validate_order() accepts below
from dataclasses import dataclass  # => @dataclass generates PriceRule's __init__ from its two fields


@dataclass(frozen=True)  # => a single validation rule, declared as data (mirrors ex-54's declarative style)
class PriceRule:  # => frozen=True -- a declared rule is a fact, never edited in place
    name: str  # => the rule's identifier, returned by validate_order() when this rule fails
    check: object  # => a Callable[[dict[str, object]], bool], kept as `object` to stay a plain dataclass


def rule_has_positive_price(order: dict[str, object]) -> bool:  # => a named check, used by a PriceRule below
    return float(order.get("price", -1)) > 0  # type: ignore[arg-type]  # => -1 default fails safely if price is missing


def rule_has_known_currency(order: dict[str, object]) -> bool:  # => a second named check
    return order.get("currency") in {"USD", "EUR", "GBP"}  # => membership check against the allowed set


PRICING_RULES: list[PriceRule] = [  # => THE PROBLEM: validate incoming price records against declared rules
    PriceRule("has_positive_price", rule_has_positive_price),  # => rule 1
    PriceRule("has_known_currency", rule_has_known_currency),  # => rule 2
]  # => closes the declared rule list -- adding rule 3 means appending here, not editing validate_order()


def validate_order(order: Mapping[str, object]) -> str | None:  # => declarative validation, same shape as ex-54
    for rule in PRICING_RULES:  # => walks the declared list -- no rule-specific branching written here
        if not rule.check(order):  # type: ignore[operator]  # => the first rule that fails wins
            return rule.name  # => names the specific rule that failed
    return None  # => every rule passed


def defense() -> str:  # => THE DEFENSE: grounded in the concrete functions above, not generic prose
    return (  # => opens the multi-line implicit-concatenation string returned below
        "Validating a price record against a fixed, growing set of business rules is a DECLARATIVE-"  # => names the paradigm up front
        "shaped problem: the rules in PRICING_RULES are stated as data (co-08), and validate_order() "  # => cites PRICING_RULES by name
        "just walks that list -- adding rule #3 means appending a PriceRule, never editing "  # => the concrete extension story
        "validate_order()'s own logic (co-02, OCP). An imperative if/elif chain would tangle every "  # => cites validate_order() by name
        "rule's logic into one growing function; the declarative table keeps each rule an independent, "  # => names the alternative and its cost
        "testable unit (see rule_has_positive_price, rule_has_known_currency), which is exactly what "  # => cites both check functions by name
        "matching-paradigm-to-problem (co-23) means in practice."  # => closes the argument by naming the guiding concept
    )  # => closes the returned string -- every claim above is grounded in a concrete name from this file


good_order = {"price": 9.99, "currency": "USD"}  # => passes every rule
bad_order = {"price": -1, "currency": "USD"}  # => fails the first rule

print(validate_order(good_order))  # => no rule failed
# => Output: None
print(validate_order(bad_order))  # => names the specific failing rule
# => Output: has_positive_price
print("PRICING_RULES" in defense() and "validate_order" in defense())  # => the defense cites real code
# => Output: True
