"""Example 43: A Validation Pipeline as a Handler Chain."""

import abc  # => imports the abc module


class ValidationHandler(abc.ABC):  # => one validation RULE, chained to the next rule
    def __init__(self) -> None:  # => the constructor
        self._next: "ValidationHandler | None" = None  # => the NEXT rule in the pipeline

    def set_next(self, handler: "ValidationHandler") -> "ValidationHandler":  # => wires the chain
        self._next = handler  # => remembers who runs after this rule
        return handler  # => returned so calls can be chained: a.set_next(b).set_next(c)

    def validate(self, value: str) -> str | None:  # => None means "passed every rule"
        error: str | None = self._check(value)  # => THIS rule's own check, run first
        if error is not None:  # => the FIRST failure stops the entire chain immediately
            return error  # => returns this value to the caller
        if self._next is not None:  # => this rule passed -- let the NEXT rule run
            return self._next.validate(value)  # => returns this value to the caller
        return None  # => every rule in the chain passed

    @abc.abstractmethod
    def _check(self, value: str) -> str | None:  # => no body -- required by every rule
        ...  # => the ellipsis stub -- concrete rules below fill this in


class NotEmptyRule(ValidationHandler):  # => runs FIRST in the pipeline
    def _check(self, value: str) -> str | None:  # => defines the _check() method
        return "value must not be empty" if value == "" else None  # => returns this value


class MinLengthRule(ValidationHandler):  # => runs SECOND, only if NotEmptyRule passed
    def _check(self, value: str) -> str | None:  # => defines the _check() method
        return "value must be at least 4 characters" if len(value) < 4 else None  # => returns this value to the caller


class AlphaOnlyRule(ValidationHandler):  # => runs THIRD, only if the first two passed
    def _check(self, value: str) -> str | None:  # => defines the _check() method
        return "value must be alphabetic" if not value.isalpha() else None  # => returns this


not_empty: NotEmptyRule = NotEmptyRule()  # => constructs not_empty
min_length: MinLengthRule = MinLengthRule()  # => constructs min_length
alpha_only: AlphaOnlyRule = AlphaOnlyRule()  # => constructs alpha_only
not_empty.set_next(min_length).set_next(alpha_only)  # => wires the pipeline in ONE expression

print(not_empty.validate(""))  # => fails the VERY FIRST rule -- the chain stops here
# => Output: value must not be empty
print(not_empty.validate("ab"))  # => passes rule 1, fails rule 2 -- rule 3 never runs
# => Output: value must be at least 4 characters
print(not_empty.validate("abcd"))  # => passes every rule in the pipeline
# => Output: None
# => The FIRST failing rule stops the chain immediately -- later rules never even run on bad input
