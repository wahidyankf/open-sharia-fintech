"""Example 20: Multi-Paradigm One File."""

from dataclasses import dataclass


@dataclass  # => OO: a class bundling state (price, qty) with behavior (subtotal)
class LineItem:
    price: int  # => unit price in cents
    qty: int  # => how many units

    def subtotal(self) -> int:  # => behavior tied to this object's own state
        return self.price * self.qty  # => the OO piece of this pipeline


def even_squares(upper: int):  # => FUNCTIONAL/declarative-flavored: a generator, lazily yields values
    return (n * n for n in range(upper) if n % 2 == 0)  # => a comprehension -- states WHAT, not a loop


items = [LineItem(100, 2), LineItem(50, 3)]  # => OO objects: two line items
subtotals = [item.subtotal() for item in items]  # => comprehension consuming OO objects together
print(subtotals)  # => [100*2, 50*3]
# => Output: [200, 150]

squares_gen = even_squares(6)  # => build the generator -- NOTHING has run yet (lazy)
squares_list = list(squares_gen)  # => draining the generator is what actually runs the computation
print(squares_list)  # => 0, 4, 16 for n in 0, 2, 4
# => Output: [0, 4, 16]

print(sum(subtotals) == 350 and squares_list == [0, 4, 16])  # => all three paradigms agree, one script
# => Output: True
