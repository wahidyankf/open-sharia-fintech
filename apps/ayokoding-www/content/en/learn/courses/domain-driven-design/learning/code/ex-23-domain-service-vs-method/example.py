# => Keeps this domain step explicit and reviewable.
"""Example 23: neither account owns a two-account rule."""


# => Gives domain rules a single, named home.
class Account:
    # => Establishes valid state before callers can rely on it.
    def __init__(self, id: str) -> None:
        self.id = id  # => an account names itself only


# => Names policy so callers do not recreate the rule.
def same_owner(left: Account, right: Account, owners: dict[str, str]) -> bool:
    # => Returns the domain result instead of leaking representation.
    return (
        # => Keeps this domain step explicit and reviewable.
        owners[left.id] == owners[right.id]
    )  # => the service uses information from both roots


# => Proves the stated business rule is observable.
assert same_owner(Account("a"), Account("b"), {"a": "u", "b": "u"})
