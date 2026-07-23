"""Example 29: Read a Table's Primary Key From Metadata."""  # => this concept

import dataclasses  # => frozen dataclasses model immutable metadata records


@dataclasses.dataclass(frozen=True)  # => co-09: one registered table's metadata
class TableMeta:  # => holds columns AND which one is the primary key
    name: str  # => the table name
    columns: tuple[str, ...]  # => ordered column names
    primary_key: str  # => the pk column name -- a plain str, not re-derived by convention


def primary_key_of(meta: TableMeta) -> str:  # => co-09: the mapper reads THIS, never guesses "id"
    return meta.primary_key  # => a direct field read -- no "assume the first column" convention


orders_meta = TableMeta(  # => a table whose pk is NOT its first column, on purpose
    name="orders",  # => table name
    columns=("total", "customer_id", "id"),  # => "id" is registered LAST here
    primary_key="id",  # => explicit -- the mapper never has to guess from column position
)  # => the closing brace of a frozen, fully-specified metadata literal
pk = primary_key_of(orders_meta)  # => reads the pk back out, explicitly
assert pk == "id"  # => correct even though "id" is not columns[0]
assert orders_meta.columns.index(pk) == 2  # => proves position was NOT used to find the pk
print(pk)  # => Output: id
