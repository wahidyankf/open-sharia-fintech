"""Example 52: A Column's Registered Python Type Drives Its Coercer."""  # => this concept

import dataclasses  # => frozen dataclasses model immutable metadata records
from typing import Any, Callable  # => the coercer registry maps types to explicitly-typed converters


@dataclasses.dataclass(frozen=True)  # => co-09: a column now ALSO carries its Python type
class Column:  # => extends Example 27's Column with a type annotation
    name: str  # => the column name, as before
    python_type: type  # => co-12: THIS is what selects the coercer -- not a separate lookup table


def _coerce_bool(raw: Any) -> bool:  # => matches Example 36's bool coercion, now a named, typed function
    return raw != 0  # => nonzero driver ints coerce to True


def _coerce_str(raw: Any) -> str:  # => TEXT columns need no conversion at all
    return raw  # => passed through unchanged


COERCERS: dict[type, Callable[[Any], Any]] = {  # => co-12: one converter PER Python type, keyed by that type
    bool: _coerce_bool,  # => explicitly-typed callables -- no untyped lambda anywhere
    str: _coerce_str,  # => same registry shape as Example 39, fully typed this time
}  # => adding a new Python type means adding ONE entry here


def coerce_by_column_type(column: Column, raw: Any) -> Any:  # => co-12 + co-09: metadata DRIVES the coercer
    coercer = COERCERS[column.python_type]  # => picks the converter using the column's OWN declared type
    return coercer(raw)  # => runs it -- no separate "is this a bool column" check anywhere else


is_active_column = Column(name="is_active", python_type=bool)  # => registered with python_type=bool
name_column = Column(name="name", python_type=str)  # => registered with python_type=str
coerced_bool = coerce_by_column_type(is_active_column, 1)  # => routed to the bool coercer, via metadata
coerced_str = coerce_by_column_type(name_column, "Alice")  # => routed to the str coercer, via metadata
assert coerced_bool is True  # => the bool column's raw 1 became a real True
assert coerced_str == "Alice"  # => the str column passed through untouched
print(coerced_bool, coerced_str)  # => Output: True Alice
