"""Example 54: Declarative Validation Rules."""

from collections.abc import Callable, Mapping  # => types the check function every Rule below carries
from dataclasses import dataclass  # => @dataclass generates Rule's __init__ from its two fields


@dataclass(frozen=True)  # => each rule is a plain DATA record: a name plus a check function
class Rule:  # => frozen=True makes every Rule immutable once constructed
    name: str  # => the label reported when this rule fails
    check: Callable[[Mapping[str, object]], bool]  # => returns True if the input satisfies this rule


RULES: list[Rule] = [  # => the whole validation policy STATED as a list of data, not a chain of ifs
    Rule("has_email", lambda data: "email" in data),  # => rule #1: the key must be present at all
    Rule("email_has_at_sign", lambda data: "@" in str(data.get("email", ""))),  # => rule #2: crude shape check
    Rule("age_is_non_negative", lambda data: int(data.get("age", 0)) >= 0),  # => rule #3: a range constraint  # type: ignore[call-overload]
]  # => closes the declared policy -- adding a rule means appending one more line here


def validate(data: Mapping[str, object]) -> str | None:  # => evaluate the rule list declaratively
    for rule in RULES:  # => walk the declared rules in order
        if not rule.check(data):  # => the first rule that fails IS the answer
            return rule.name  # => report exactly which declared rule was violated
    return None  # => every declared rule passed


good_input = {"email": "a@example.com", "age": 30}  # => passes every rule
bad_input = {"email": "not-an-email", "age": 30}  # => fails the second rule specifically

print(validate(good_input))  # => no rule failed
# => Output: None
print(validate(bad_input))  # => names the exact failing rule
# => Output: email_has_at_sign
