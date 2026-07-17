"""Example 14: Creator: Order Creates Its Own OrderLine."""  # => module docstring

from dataclasses import dataclass  # => imports dataclass from dataclasses


@dataclass  # => generates __init__ from the fields below
class OrderLine:  # => a single line item Order aggregates and owns
    item: str  # => the item name, part of the generated __init__
    quantity: int  # => how many units, part of the generated __init__
    unit_price: float  # => price per unit, part of the generated __init__


class Order:  # => the CREATOR: Order aggregates OrderLine, so Order builds them
    def __init__(self) -> None:  # => the constructor
        self.lines: list[OrderLine] = []  # => the collection Order aggregates
        # => GRASP's Creator rule: whoever aggregates B is the natural creator of B

    def add_line(  # => the CREATION method, spread across lines to annotate each field
        self,
        item: str,  # => raw field data, not a pre-built OrderLine
        quantity: int,  # => raw field data, not a pre-built OrderLine
        unit_price: float,
        # => the CALLER never constructs OrderLine directly -- Order does it instead
    ) -> OrderLine:  # => the creation method lives HERE, on the aggregating class
        line: OrderLine = OrderLine(item, quantity, unit_price)  # => Order builds the object it aggregates
        self.lines.append(line)  # => and immediately owns it in its own collection
        return line  # => returns the built object for the caller's convenience


order: Order = Order()  # => constructs order
line: OrderLine = order.add_line(
    "widget",  # => item name, raw data passed to the Creator
    3,  # => quantity, raw data passed to the Creator
    4.5,  # => unit price, raw data passed to the Creator
    # => the caller never writes OrderLine(...) itself -- Order builds it internally
)  # => the caller never writes OrderLine(...) itself

print(line)  # => confirms Order built a real, well-formed OrderLine
print(order.lines[0] is line)  # => the SAME object Order created and now holds
# => not a copy -- Order's own collection holds the very object it just built
# => Output: OrderLine(item='widget', quantity=3, unit_price=4.5)
# => True
# => `Order.add_line()` is the Creator: it both builds the OrderLine and aggregates it in one step
