"""Example 27: Register Table Metadata."""  # => names the concept under test

import dataclasses  # => frozen dataclasses model immutable metadata records


@dataclasses.dataclass(frozen=True)  # => co-09: metadata is a value, registered once, read many times
class Column:  # => one column's name -- the builder and mapper both read from this
    name: str  # => the only field this minimal column record needs


@dataclasses.dataclass(frozen=True)  # => the shared schema record both builder and mapper consult
class TableMeta:  # => one table's full metadata: its columns and its primary key
    name: str  # => the table name, e.g. "users"
    columns: tuple[Column, ...]  # => ordered column list -- registration order is column order
    primary_key: str  # => the primary-key column name, read back out in Example 29


registry: dict[str, TableMeta] = {}  # => the CENTRAL registry -- one place, never duplicated per caller


def register_table(meta: TableMeta) -> None:  # => the single write path into the registry
    registry[meta.name] = meta  # => keyed by table name -- overwrites a stale re-registration


users_meta = TableMeta(  # => register "users" ONCE, with its full column list and pk
    name="users",  # => table name -- the registry key
    columns=(Column(name="id"), Column(name="name"), Column(name="email")),  # => 3 columns, in order
    primary_key="id",  # => which column is the pk -- Example 29 reads this back
)  # => TableMeta is frozen -- this literal is the ONLY way "users" metadata gets built
register_table(users_meta)  # => later readers look this up by name, not by re-declaring it

fetched = registry["users"]  # => a fresh lookup, simulating a caller elsewhere in the codebase
assert fetched is users_meta  # => the registry stores the SAME object
# => no copying happened on read -- registry[name] is a plain dict lookup, nothing more
column_names = [c.name for c in fetched.columns]  # => reads the column list back out
print(column_names)  # => Output: ['id', 'name', 'email']
