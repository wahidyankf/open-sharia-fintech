"""Example 13: Information Expert: Order Owns Its Total."""  # => module docstring

from dataclasses import dataclass  # => imports dataclass from dataclasses


@dataclass  # => generates __init__ from the fields below, no hand-written boilerplate
class OrderLine:  # => a single line item -- quantity and unit price, nothing more
    item: str  # => the item name, part of the generated __init__
    quantity: int  # => how many units, part of the generated __init__
    unit_price: float  # => price per unit, part of the generated __init__


class Order:  # => the class that OWNS the line items -- the "information expert"
    def __init__(self) -> None:  # => the constructor
        self.lines: list[OrderLine] = []  # => Order holds every line item it needs

    def add_line(self, line: OrderLine) -> None:  # => defines the add_line() method
        self.lines.append(line)  # => appends to Order's OWN collection

    def total(self) -> float:  # => Order computes its OWN total -- it has the data
        return sum(  # => builds the sum via a generator expression, no helper function
            line.quantity * line.unit_price  # => the per-line subtotal being summed
            for line in self.lines
            # => the information EXPERT is whichever class already holds the data
        )  # => no external function ever loops over Order's lines to do this


order: Order = Order()  # => constructs order
order.add_line(OrderLine("widget", 2, 9.99))  # => adds the first line item
order.add_line(OrderLine("gadget", 1, 19.99))  # => adds a second, different line item

print(round(order.total(), 2))  # => Order alone answers "what is my total?"
# => Output: 39.97
# => Order holds the line items, so Order -- not some external loop -- is the natural place for total()
