"""Example 18: test names can read as business rules."""


class Customer:
    def __init__(self, credit: int) -> None:
        self.credit = credit

    def can_spend(self, amount: int) -> bool:
        return amount <= self.credit  # => domain predicate


def test_customer_cannot_exceed_credit_limit() -> None:
    assert not Customer(100).can_spend(
        101
    )  # => the test sentence mirrors the expert rule


test_customer_cannot_exceed_credit_limit()
print("domain sentence passes")
