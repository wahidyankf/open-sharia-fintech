"""Example 53: Bloom Filters Reduce Read Amplification."""
# A Bloom filter (co-15) has NO false negatives -- "maybe present" opens the table, "absent" skips it.

import hashlib  # => stdlib hashing, used to build a tiny illustrative Bloom filter
from dataclasses import dataclass, field  # => a typed SSTable with an attached filter


def bloom_bits(
    key: str, size: int
) -> set[int]:  # => two independent hash positions per key
    h1 = (
        int(hashlib.md5(key.encode()).hexdigest(), 16) % size
    )  # => first hash function's bit position
    h2 = (
        int(hashlib.sha1(key.encode()).hexdigest(), 16) % size
    )  # => second, independent hash position
    return {h1, h2}  # => this key sets (or checks) exactly these two bits


@dataclass  # => a plain, typed record -- fields carry their own default_factory
class SSTable:  # => a sorted segment, now with its own Bloom filter attached
    data: dict[str, str] = field(
        default_factory=dict[str, str]
    )  # => the actual key-value contents
    filter_bits: set[int] = field(
        default_factory=set[int]
    )  # => bits set by every key this table holds

    def add(
        self, key: str, value: str
    ) -> None:  # => insert a key AND mark its Bloom bits
        self.data[key] = value  # => the real data
        self.filter_bits |= bloom_bits(
            key, size=64
        )  # => union in this key's two bit positions

    def might_contain(
        self, key: str
    ) -> bool:  # => the filter check -- no false negatives, ever
        return (
            bloom_bits(key, size=64) <= self.filter_bits
        )  # => both bits must already be set


def point_read(
    key: str, tables: list[SSTable]
) -> tuple[str | None, int]:  # => (value, tables OPENED)
    opened = 0  # => only counts tables actually opened -- a filter skip costs nothing
    for table in reversed(tables):  # => newest first, as always
        if not table.might_contain(
            key
        ):  # => the filter proves this table cannot have the key
            continue  # => SKIPPED -- no table open, no read amplification incurred here
        opened += (
            1  # => the filter said "maybe" -- must actually open and check this table
        )
        if key in table.data:  # => confirm the filter's "maybe" against the real data
            return table.data[
                key
            ], opened  # => confirmed present -- stop scanning further tables
    return (
        None,
        opened,
    )  # => genuinely absent from every table that wasn't filter-skipped


tables = [
    SSTable() for _ in range(5)
]  # => five SSTables, none of which will ever hold "missing-key"
for i, table in enumerate(tables):  # => populate each with unrelated keys
    table.add(f"key-{i}", f"value-{i}")  # => populate this table with one unrelated key

_, opened = point_read(
    "missing-key", tables
)  # => a lookup the filters should mostly skip
print(opened)  # => Output: 0

assert opened < len(
    tables
)  # => fewer tables were opened than exist -- the filters did their job
print("ex-53 OK")  # => Output: ex-53 OK
