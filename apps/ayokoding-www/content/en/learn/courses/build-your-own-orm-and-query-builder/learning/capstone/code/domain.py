# pyright: strict
"""Capstone: domain.py -- the two mapped types every other module in this capstone shares:
Customer (the parent) and Order (the child, via customer_id). Plain mutable dataclasses --
mapper.py (co-10, co-11) reads and writes their fields; unit_of_work.py (co-16..co-19)
snapshots and tracks them; lazy.py (co-21) attaches a lazy relationship on top of Customer
without touching these two field definitions at all.
"""

import dataclasses
import datetime


@dataclasses.dataclass  # => mutable -- unit_of_work.py needs to mutate a LOADED object to detect co-17 dirt
class Customer:
    id: int | None  # => None until unit_of_work.py's flush() assigns a real primary key
    name: str
    email: str


@dataclasses.dataclass
class Order:
    id: int | None  # => None until flush() assigns a real primary key
    customer_id: int  # => the FK back to Customer.id -- co-19's flush ordering depends on this
    item: str
    amount: float
    placed_on: datetime.date  # => co-12: mapper.py coerces this to/from SQLite's TEXT storage
