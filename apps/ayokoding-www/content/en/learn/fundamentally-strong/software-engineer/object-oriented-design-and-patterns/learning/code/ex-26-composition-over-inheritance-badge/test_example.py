"""Example 26: pytest verification for Composition Over Inheritance: Model a Badge as Has-A."""

from example import Badge, User


def test_user_class_never_gains_subclasses_for_new_badge_kinds() -> None:
    gold_user: User = User("Alice", [Badge("gold", "Top Seller")])
    silver_user: User = User("Bob", [Badge("silver", "Rising Star")])
    # => a brand-new "platinum" distinction needed ZERO new classes, just a new Badge value
    platinum_user: User = User("Carol", [Badge("platinum", "Legend")])
    assert User.__subclasses__() == []  # => no GoldUser, SilverUser, or PlatinumUser exists
    assert type(gold_user) is type(silver_user) is type(platinum_user)  # => one shared class


def test_describe_reflects_each_users_own_badges() -> None:
    gold_user: User = User("Alice", [Badge("gold", "Top Seller")])
    assert gold_user.describe() == "Alice (Top Seller)"


# => Run: pytest -- Output: 2 passed
