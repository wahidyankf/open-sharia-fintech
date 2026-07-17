"""Example 26: Composition Over Inheritance: Model a Badge as Has-A."""  # => docstring

from dataclasses import dataclass  # => imports dataclass from dataclasses


@dataclass  # => generates __init__ from the fields below
class Badge:  # => a small, independent value -- NOT a base class anyone inherits from
    color: str  # => the badge's color, part of the generated __init__
    label: str  # => the badge's label, part of the generated __init__


class User:  # => a SINGLE class, regardless of how many badge combinations exist
    # => has-a: User HOLDS badges; it never becomes GoldUser, SilverUser, and so on
    def __init__(  # => the constructor, spread across lines to annotate each field
        self,  # => the User instance being constructed
        name: str,  # => a plain string field, unrelated to the has-a relationship
        badges: list[Badge],
        # => badges is a HAS-A relationship -- User holds Badge objects, never inherits them
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self.name = name  # => stores name on this instance
        self.badges = badges  # => stores the badge LIST, not a subclass identity

    def describe(self) -> str:  # => defines the describe() method
        labels: str = ", ".join(
            badge.label  # => extracts just the label text from each Badge value
            for badge in self.badges  # => reads whatever badges THIS user has
        )  # => reads badge data without needing a GoldUser or SilverUser subclass
        return f"{self.name} ({labels})" if labels else self.name  # => handles no badges too


gold_user: User = User(
    "Alice",  # => the name field, plain data
    [Badge("gold", "Top Seller")],  # => the DATA changes; the class never does
)  # => a "gold" distinction via composition, NOT a GoldUser subclass
silver_user: User = User(
    "Bob",  # => the name field, plain data
    [Badge("silver", "Rising Star")],  # => a different Badge value, same User class
)  # => a DIFFERENT distinction, same User class, zero new subclasses

print(gold_user.describe())  # => confirms composition produced the right description
print(silver_user.describe())  # => confirms a totally different badge, same User class
# => inheritance would have needed GoldUser, SilverUser, and every future combination
# => Output: Alice (Top Seller)
# => Bob (Rising Star)
# => A `PlatinumUser` subclass is never needed -- `User(name, [Badge("platinum", "...")])` is enough
