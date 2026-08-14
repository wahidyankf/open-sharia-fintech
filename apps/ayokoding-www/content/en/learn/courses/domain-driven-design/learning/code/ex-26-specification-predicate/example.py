"""Example 26: a specification reifies a business predicate."""


class PremiumCustomerSpec:
    def is_satisfied_by(self, spend: int) -> bool:
        return spend >= 100  # => a named rule is reusable and testable


spec = PremiumCustomerSpec()
assert spec.is_satisfied_by(120) and not spec.is_satisfied_by(99)
