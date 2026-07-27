"""Example 46: Clustered Index -- Leaf Holds the Full Row."""
# A clustered index (co-27) stores the full row directly in the leaf.

from dataclasses import dataclass  # => a plain, typed row


@dataclass  # => a plain, typed record -- no custom __init__ needed
class Row:  # => a full table row, exactly as it would be stored
    id: int  # => the primary key -- also this row's clustering key
    name: str  # => an ordinary column, stored right alongside the PK
    email: str  # => another ordinary column, stored right alongside the PK


fetch_count: int = (
    0  # => counts SEPARATE storage fetches -- a clustered lookup should need only one
)


def clustered_lookup(
    index: dict[int, Row], pk: int
) -> Row | None:  # => co-27: leaf itself holds the row
    global fetch_count  # => a module-level counter, mutated here to measure fetch cost
    fetch_count += (
        1  # => ONE fetch: the leaf lookup IS the row fetch, nothing further to do
    )
    return index.get(pk)  # => the full row comes back directly from the index entry


index: dict[
    int, Row
] = {  # => the clustered index -- keyed by PK, VALUED by the entire row
    1: Row(
        id=1, name="Alice", email="alice@example.com"
    ),  # => the leaf entry for PK 1 IS the whole row
    2: Row(
        id=2, name="Bob", email="bob@example.com"
    ),  # => same for PK 2 -- no separate heap exists
}  # => end of the clustered-index fixture

fetch_count = 0  # => reset before measuring this specific lookup
row = clustered_lookup(index, pk=1)  # => a single primary-key lookup
print(row)  # => Output: Row(id=1, name='Alice', email='alice@example.com')
print(fetch_count)  # => Output: 1

assert row is not None and row.name == "Alice"  # => the correct row came back
assert (
    fetch_count == 1
)  # => exactly one fetch -- no second trip to a separate heap was ever needed
print("ex-46 OK")  # => Output: ex-46 OK
