"""Example 72: A Frozen Money Whose Arithmetic Returns New Instances."""

from dataclasses import dataclass  # => imports dataclass from dataclasses


@dataclass(frozen=True)  # => generates boilerplate methods from the field list below
class Money:  # => begins the Money class body
    amount: int  # => integer cents -- immutable once constructed

    def plus(self, other: "Money") -> "Money":  # => never mutates self OR other
        return Money(self.amount + other.amount)  # => always returns a BRAND-NEW Money


a: Money = Money(500)  # => constructs a
b: Money = Money(300)  # => constructs b
c: Money = a.plus(b)  # => a new object, computed from a and b
print(a.amount, b.amount, c.amount)  # => neither operand changed; only c holds the sum
# => Output: 500 300 800
# => `a.plus(b)` cannot mutate `a` or `b` even if it tried
