"""Example 37: Chaining map, filter, and reduce."""

from functools import reduce  # => reduce folds the filtered stream into one total

orders = [12, 7, 25, 3, 18, 9]  # => raw order amounts, some too small to matter

doubled = map(
    lambda amount: amount * 2, orders
)  # => LAZY: doubles every order (e.g. a 2x promo)
significant = filter(
    lambda amount: amount > 20, doubled
)  # => LAZY: keeps only large-enough orders
total = reduce(
    lambda acc, amount: acc + amount, significant, 0
)  # => folds survivors into one sum
# => each stage is lazy until reduce finally pulls every value through the whole pipeline

manual_total = sum(
    a * 2 for a in orders if a * 2 > 20
)  # => the equivalent single comprehension

print(total)  # => Output: 110
print(
    total == manual_total
)  # => Output: True -- three separate stages, one verified answer
