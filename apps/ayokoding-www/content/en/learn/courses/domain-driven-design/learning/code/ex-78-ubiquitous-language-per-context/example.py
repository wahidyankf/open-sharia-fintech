# => Keeps this domain step explicit and reviewable.
"""Example 78: context-local tests preserve context-local meanings."""


# => Names policy so callers do not recreate the rule.
def identity_account_allows_login(password_ok: bool) -> bool:
    return password_ok  # => Identity's account means login


# => Names policy so callers do not recreate the rule.
def billing_account_has_balance(balance: int) -> bool:
    return balance >= 0  # => Billing's account means ledger


# => Proves the stated business rule is observable.
assert identity_account_allows_login(True) and billing_account_has_balance(0)
