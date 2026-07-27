"""Example 52: Measure Space Amplification."""
# Space amplification (co-14) is on-disk bytes / live (current, non-stale) bytes.

from dataclasses import dataclass  # => a typed SSTable representation


@dataclass  # => a plain, typed record -- no custom __init__ needed
class SSTable:  # => a sorted, immutable segment that may contain STALE (overwritten) values
    data: dict[
        str, str
    ]  # => key -> value, some of which may be superseded by a later table


def on_disk_bytes(
    tables: list[SSTable],
) -> int:  # => EVERY byte physically stored, stale or not
    return sum(
        len(k) + len(v) for table in tables for k, v in table.data.items()
    )  # => no dedup at all


def live_bytes(
    tables: list[SSTable],
) -> int:  # => only the bytes a user's read would actually see
    live: dict[
        str, str
    ] = {}  # => the current, deduplicated view -- newest value per key wins
    for (
        table
    ) in tables:  # => oldest to newest, so later tables correctly override earlier ones
        live.update(
            table.data
        )  # => co-12's newest-wins rule, applied across ALL tables at once
    return sum(
        len(k) + len(v) for k, v in live.items()
    )  # => bytes needed for just the live data


tables = [  # => two tables where the first key ('a') has been overwritten once
    SSTable(
        data={"a": "original-value"}
    ),  # => this "a" is now STALE -- superseded below
    SSTable(
        data={"a": "updated-value", "b": "v1"}
    ),  # => the CURRENT value for "a", plus a fresh key
]  # => end of the tables fixture
disk = on_disk_bytes(
    tables
)  # => counts BOTH copies of "a" -- the stale one and the current one
live = live_bytes(tables)  # => counts only the single, current copy of "a", plus "b"
amplification = disk / live  # => the exact ratio the spec asks to verify
print(disk)  # => Output: 32
print(live)  # => Output: 17
print(round(amplification, 2))  # => Output: 1.88

assert (
    amplification > 1
)  # => a stale version inflated on-disk bytes beyond what live data needs
print("ex-52 OK")  # => Output: ex-52 OK
