# pyright: strict
"""Capstone: metadata.py -- a central table/column metadata registry (co-09), plus one
concrete type coercion (co-12) the mapper.py step reads from: customer_order.placed_on is
stored as SQLite TEXT (an ISO date string, since SQLite has no native DATE type) but the
domain object always sees a real datetime.date. This module is the ONE place that fact is
recorded -- both the builder and the mapper would drift apart silently without it.
"""

import dataclasses
import datetime


@dataclasses.dataclass(frozen=True)  # => co-09: metadata is itself immutable, read-only data
class TableMeta:
    name: str  # => the SQL table name
    columns: tuple[str, ...]  # => co-09: every column, in a fixed order -- the ONE source of truth
    primary_key: str  # => co-09: which column identity_map.py and unit_of_work.py key writes by


CUSTOMER = TableMeta(  # => co-09: registered once, read everywhere below
    name="customer",
    columns=("id", "name", "email"),
    primary_key="id",
)

CUSTOMER_ORDER = TableMeta(  # => co-09: the child table -- customer_id is its FK back to CUSTOMER
    name="customer_order",
    columns=("id", "customer_id", "item", "amount", "placed_on"),
    primary_key="id",
)


def coerce_date_on_load(raw: str) -> datetime.date:  # => co-12: driver TEXT -> domain date, on the way IN
    return datetime.date.fromisoformat(raw)  # => SQLite stores no native DATE type -- this IS the coercion


def coerce_date_on_store(value: datetime.date) -> str:  # => co-12: the INVERSE, on the way OUT
    return value.isoformat()  # => back to the ISO TEXT SQLite actually stores


if __name__ == "__main__":  # => guards against running the demo on `import metadata`
    print(CUSTOMER.columns)  # => Output: ('id', 'name', 'email')
    print(CUSTOMER.primary_key)  # => Output: id
    round_tripped = coerce_date_on_load(coerce_date_on_store(datetime.date(2026, 7, 18)))
    print(round_tripped)  # => Output: 2026-07-18
    assert round_tripped == datetime.date(2026, 7, 18)  # => co-12: a full round trip changes nothing
