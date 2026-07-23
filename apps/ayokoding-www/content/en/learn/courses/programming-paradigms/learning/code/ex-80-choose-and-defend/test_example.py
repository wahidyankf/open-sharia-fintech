"""Example 80: pytest verification for Choose and Defend."""

from example import PRICING_RULES, defense, validate_order


def test_validation_matches_the_declared_rule_table() -> None:
    assert validate_order({"price": 5.0, "currency": "EUR"}) is None  # => passes every declared rule
    assert validate_order({"price": -5.0, "currency": "EUR"}) == "has_positive_price"  # => fails rule #1
    assert validate_order({"price": 5.0, "currency": "XXX"}) == "has_known_currency"  # => fails rule #2


def test_defense_references_concrete_functions_not_generic_prose() -> None:
    text = defense()
    assert "PRICING_RULES" in text  # => names the actual data structure this example built
    assert "validate_order" in text  # => names the actual function this example built
    assert len(PRICING_RULES) == 2  # => the defense's claims are checked against the real rule count


# => Run: pytest -- Output: 2 passed
