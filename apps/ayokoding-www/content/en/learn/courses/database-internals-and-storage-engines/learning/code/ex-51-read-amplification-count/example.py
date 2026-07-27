"""Example 51: Count Read Amplification."""
# Read amplification (co-14) counts SSTables actually opened to answer one point read.

from dataclasses import dataclass  # => a typed SSTable representation


@dataclass  # => a plain, typed record -- no custom __init__ needed
class SSTable:  # => a sorted, immutable segment -- newest tables are checked first
    data: dict[str, str]  # => key -> value


def point_read(
    key: str, tables: list[SSTable]
) -> tuple[str | None, int]:  # => returns (value, tables touched)
    touched = 0  # => how many SSTables this read had to open
    for table in reversed(tables):  # => newest first -- co-12's newest-wins rule
        touched += 1  # => opening this table counts as one unit of read amplification
        if key in table.data:  # => found it -- no need to check any older table
            return table.data[
                key
            ], touched  # => found -- stop, no need to check older tables
    return None, touched  # => the key exists in none of the tables checked


few_tables = [
    SSTable(data={"a": "v1"})
]  # => one segment -- a miss touches just one table
many_tables = [
    SSTable(data={"x": str(i)}) for i in range(5)
]  # => five segments, none contain "a"

_, touched_few = point_read("a", few_tables)  # => a miss against a single-table set
_, touched_many = point_read("a", many_tables)  # => a miss against a five-table set
print(touched_few)  # => Output: 1
print(touched_many)  # => Output: 5

assert (
    touched_many > touched_few
)  # => read amplification grows with segment count, exactly as expected
print("ex-51 OK")  # => Output: ex-51 OK
