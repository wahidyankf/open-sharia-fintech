# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Worked Example 14: the shell combines an effect with a pure calculation."""


# => This keeps the modeled rule explicit so its trade-off can be inspected.
class Totals:
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    def subtotal(self, order_id: str) -> int:
        # => This keeps the modeled rule explicit so its trade-off can be inspected.
        return 100


# => This keeps the modeled rule explicit so its trade-off can be inspected.
def quote(repository: Totals, order_id: str) -> int:
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    subtotal = repository.subtotal(order_id)
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    return subtotal - subtotal * 10 // 100


# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(quote(Totals(), "order-1"))
