# pyright: strict
"""Capstone: mapper.py -- row-to-object (co-10) and object-to-row (co-11) mapping for
Customer and Order, reading the column order metadata.py registered (co-09) and applying
metadata.py's date coercion (co-12) on Order.placed_on. This is the ONE place a schema
change to either table has to be updated -- unit_of_work.py never assembles a row by hand.
"""

from typing import Any

from domain import Customer, Order
from metadata import coerce_date_on_load, coerce_date_on_store


def load_customer(row: tuple[Any, ...]) -> Customer:  # => co-10: driver tuple -> typed object
    return Customer(id=row[0], name=row[1], email=row[2])  # => assignment BY COLUMN ORDER (metadata.CUSTOMER)


def load_order(row: tuple[Any, ...]) -> Order:  # => co-10 + co-12: driver tuple -> typed object, date coerced
    return Order(
        id=row[0],
        customer_id=row[1],
        item=row[2],
        amount=row[3],
        placed_on=coerce_date_on_load(row[4]),  # => co-12: TEXT -> date, ONLY here, never left to the caller
    )


def customer_to_values(customer: Customer) -> dict[str, Any]:  # => co-11: object -> INSERT/UPDATE-ready dict
    return {"name": customer.name, "email": customer.email}  # => pk excluded -- the database assigns it


def order_to_values(order: Order) -> dict[str, Any]:  # => co-11 + co-12: object -> row dict, date coerced back
    return {
        "customer_id": order.customer_id,
        "item": order.item,
        "amount": order.amount,
        "placed_on": coerce_date_on_store(order.placed_on),  # => co-12: date -> TEXT, the INVERSE of load_order
    }


if __name__ == "__main__":  # => guards against running the demo on `import mapper`
    import datetime

    customer = load_customer((1, "Ada", "ada@example.com"))
    print(customer)  # => Output: Customer(id=1, name='Ada', email='ada@example.com')
    order = load_order((10, 1, "Keyboard", 79.5, "2026-07-18"))
    print(order)  # => Output: Order(id=10, customer_id=1, item='Keyboard', amount=79.5, placed_on=datetime.date(2026, 7, 18))
    assert order.placed_on == datetime.date(2026, 7, 18)  # => co-12: the mapper coerced TEXT into a real date
    round_trip = order_to_values(order)
    print(round_trip)  # => Output: {'customer_id': 1, 'item': 'Keyboard', 'amount': 79.5, 'placed_on': '2026-07-18'}
    assert round_trip["placed_on"] == "2026-07-18"  # => co-12: coerced back to the driver-native TEXT form
