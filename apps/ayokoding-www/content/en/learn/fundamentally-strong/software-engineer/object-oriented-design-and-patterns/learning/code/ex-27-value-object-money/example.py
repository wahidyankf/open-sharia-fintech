"""Example 27: Value Object: Immutable Money with Value Equality."""

from dataclasses import dataclass  # => imports dataclass from dataclasses


@dataclass(frozen=True)  # => frozen=True makes every field read-only after construction
class Money:  # => a VALUE object -- every method here concerns ONLY a monetary amount
    amount: int  # => stored in cents, part of the generated __init__
    currency: str  # => the currency code, part of the generated __init__

    def add(self, other: "Money") -> "Money":  # => never mutates self -- returns a NEW Money
        if self.currency != other.currency:  # => guards against mixing currencies
            raise ValueError("currency mismatch")  # => rejects the call entirely
        return Money(self.amount + other.amount, self.currency)  # => a fresh, independent Money -- neither operand was touched


ten_usd: Money = Money(1000, "usd")  # => $10.00, immutable from the moment it's built
five_usd: Money = Money(500, "usd")  # => a second, independent Money value

total: Money = ten_usd.add(five_usd)  # => produces a THIRD Money -- the first two are unchanged
print(total)  # => the generated __repr__ shows every field explicitly
# => Output: Money(amount=1500, currency='usd')

same_value: Money = Money(1000, "usd")  # => a SEPARATE object with identical field values
print(ten_usd == same_value, ten_usd is same_value)  # => value equality, NOT identity
# => Output: True False
# => `@dataclass(frozen=True)` gives `Money` value-based `__eq__` for free -- two equal amounts always compare equal
