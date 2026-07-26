"""Example 47: Heap Table + Secondary Index via (page, slot) Pointer."""
# A heap table's secondary index (co-27) stores only a pointer, not the row.

from dataclasses import dataclass  # => a plain, typed pointer


@dataclass(
    frozen=True
)  # => immutable -- a pointer value should never mutate after creation
class RowPointer:  # => a secondary index entry never stores the row itself -- only WHERE to find it
    page: int  # => which heap page the row physically lives on
    slot: int  # => which slot within that page's slot array (co-01/co-02 layout)


heap: dict[
    int, list[str]
] = {  # => page_id -> list of row values, indexed by slot number
    0: ["alice@example.com", "bob@example.com"],  # => page 0 holds two rows
    1: ["carol@example.com"],  # => page 1 holds one row
}  # => end of the heap fixture
secondary_index: dict[
    str, RowPointer
] = {  # => keyed by the INDEXED column (email), not the PK
    "alice@example.com": RowPointer(
        page=0, slot=0
    ),  # => points AT the heap, doesn't duplicate the row
    "bob@example.com": RowPointer(page=0, slot=1),  # => same page, different slot
    "carol@example.com": RowPointer(page=1, slot=0),  # => a different page entirely
}  # => end of the secondary-index fixture


def secondary_lookup(
    email: str,
) -> str | None:  # => co-27: two steps -- index, THEN heap fetch
    pointer = secondary_index.get(email)  # => step 1: find WHERE the row lives
    if pointer is None:  # => not found in the index at all
        return None  # => the indexed value simply does not exist
    return heap[pointer.page][
        pointer.slot
    ]  # => step 2: fetch the actual row from the heap page


result = secondary_lookup(
    "bob@example.com"
)  # => resolve through both steps to the heap row
print(result)  # => Output: bob@example.com

assert (
    result == "bob@example.com"
)  # => the secondary index correctly resolved to the heap row
assert secondary_index["bob@example.com"] == RowPointer(
    page=0, slot=1
)  # => the pointer itself is exact
print("ex-47 OK")  # => Output: ex-47 OK
