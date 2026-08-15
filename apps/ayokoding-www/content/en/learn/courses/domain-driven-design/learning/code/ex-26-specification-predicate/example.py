# => Keeps this domain step explicit and reviewable.
"""Example 26: a specification reifies a business predicate."""


# => Gives domain rules a single, named home.
class PremiumCustomerSpec:
    # => Names policy so callers do not recreate the rule.
    def is_satisfied_by(self, spend: int) -> bool:
        return spend >= 100  # => a named rule is reusable and testable


# => Keeps scenario data close to the rule it exercises.
spec = PremiumCustomerSpec()
# => Proves the stated business rule is observable.
assert spec.is_satisfied_by(120) and not spec.is_satisfied_by(99)
