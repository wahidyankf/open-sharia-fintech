"""Example 69: Declarative Mini DSL."""

from collections.abc import Callable  # => types every rule's evaluate field: a predicate over one int
from dataclasses import dataclass  # => @dataclass generates RuleExpr's __init__ from its two fields


@dataclass(frozen=True)  # => a single composable rule -- the DSL's one building block
class RuleExpr:  # => frozen=True -- composing rules always builds a NEW RuleExpr, never mutates one
    evaluate: Callable[[int], bool]  # => the rule's actual test, wrapped so it can be composed declaratively
    label: str  # => a self-describing name, built up automatically as rules compose

    def __and__(self, other: "RuleExpr") -> "RuleExpr":  # => operator overload: `&` composes two rules
        return RuleExpr(lambda n: self.evaluate(n) and other.evaluate(n), f"({self.label} AND {other.label})")  # => new composed rule

    def __or__(self, other: "RuleExpr") -> "RuleExpr":  # => operator overload: `|` composes two rules
        return RuleExpr(lambda n: self.evaluate(n) or other.evaluate(n), f"({self.label} OR {other.label})")  # => new composed rule


def gt(threshold: int) -> RuleExpr:  # => a small builder function -- the DSL's vocabulary
    return RuleExpr(lambda n: n > threshold, f"n > {threshold}")  # => builds one leaf rule, label included


def even() -> RuleExpr:  # => another builder function
    return RuleExpr(lambda n: n % 2 == 0, "n is even")  # => builds another leaf rule


composed_rule = gt(10) & even()  # => "n > 10 AND n is even" -- built declaratively via `&`, no if-chain
print(composed_rule.label)  # => the composed rule's own self-describing label
# => Output: (n > 10 AND n is even)
print(composed_rule.evaluate(12))  # => 12 > 10 and 12 is even
# => Output: True
print(composed_rule.evaluate(11))  # => 11 > 10 but 11 is odd
# => Output: False
