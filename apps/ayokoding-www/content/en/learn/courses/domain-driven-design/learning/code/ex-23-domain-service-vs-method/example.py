"""Example 23: neither account owns a two-account rule."""


class Account:
    def __init__(self, id: str) -> None:
        self.id = id  # => an account names itself only


def same_owner(left: Account, right: Account, owners: dict[str, str]) -> bool:
    return (
        owners[left.id] == owners[right.id]
    )  # => the service uses information from both roots


assert same_owner(Account("a"), Account("b"), {"a": "u", "b": "u"})
