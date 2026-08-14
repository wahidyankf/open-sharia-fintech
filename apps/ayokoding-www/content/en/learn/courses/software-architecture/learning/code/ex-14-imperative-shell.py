"""Worked Example 14: the shell combines an effect with a pure calculation."""


class Totals:
    def subtotal(self, order_id: str) -> int:
        return 100


def quote(repository: Totals, order_id: str) -> int:
    subtotal = repository.subtotal(order_id)
    return subtotal - subtotal * 10 // 100


print(quote(Totals(), "order-1"))
