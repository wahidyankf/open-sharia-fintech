"""Example 10: Buffer Pool Page-Table Lookup -- page-id maps to a resident frame."""

from dataclasses import dataclass  # => a plain, typed record for one buffer-pool frame


@dataclass
class Frame:  # => one buffer-pool slot holding a page's in-memory copy
    page_id: int  # => which on-disk page this frame currently holds
    data: bytes  # => that page's bytes, as loaded into memory


# The page table maps page_id -> Frame (co-04) -- it is the buffer pool's
# core index, and a lookup miss (returning None) is exactly the signal that
# tells a fetch it must go to disk.
page_table: dict[int, Frame] = {}  # => empty pool: nothing resident yet
page_table[7] = Frame(
    page_id=7, data=b"resident-page-7"
)  # => page 7 is loaded into the pool
page_table[9] = Frame(page_id=9, data=b"resident-page-9")  # => page 9 is loaded too

found = page_table.get(7)  # => a lookup for a RESIDENT page id
print(found)  # => Output: Frame(page_id=7, data=b'resident-page-7')
missing = page_table.get(3)  # => a lookup for a page id NOT currently resident
print(missing)  # => Output: None

assert (
    found is not None and found.page_id == 7
)  # => a resident lookup returns its own frame
assert (
    missing is None
)  # => a non-resident lookup returns None, never a stale/wrong frame
print("ex-10 OK")  # => Output: ex-10 OK
