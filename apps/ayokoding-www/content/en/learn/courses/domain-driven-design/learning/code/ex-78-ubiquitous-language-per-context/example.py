"""Example 78: context-local tests preserve context-local meanings."""


def identity_account_allows_login(password_ok: bool) -> bool:
    return password_ok  # => Identity's account means login


def billing_account_has_balance(balance: int) -> bool:
    return balance >= 0  # => Billing's account means ledger


assert identity_account_allows_login(True) and billing_account_has_balance(0)
