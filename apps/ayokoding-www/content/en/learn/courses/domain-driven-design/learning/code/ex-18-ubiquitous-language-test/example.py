# => Keeps this domain step explicit and reviewable.
"""Example 18: test names can read as business rules."""


# => Gives domain rules a single, named home.
class Customer:
    # => Establishes valid state before callers can rely on it.
    def __init__(self, credit: int) -> None:
        # => Keeps lifecycle state controlled by the domain object.
        self.credit = credit

    # => Names policy so callers do not recreate the rule.
    def can_spend(self, amount: int) -> bool:
        return amount <= self.credit  # => domain predicate


# => Names policy so callers do not recreate the rule.
def test_customer_cannot_exceed_credit_limit() -> None:
    # => Proves the stated business rule is observable.
    assert not Customer(100).can_spend(
        # => Keeps this domain step explicit and reviewable.
        101
    )  # => the test sentence mirrors the expert rule


# => Keeps this domain step explicit and reviewable.
test_customer_cannot_exceed_credit_limit()
# => Makes the demonstrated domain outcome visible.
print("domain sentence passes")
