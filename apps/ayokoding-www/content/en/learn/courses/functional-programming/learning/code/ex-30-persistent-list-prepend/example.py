"""Example 30: O(1) Sharing on a Persistent Linked List."""

from __future__ import (
    annotations,
)  # => enables the quoted 'PList | None' forward reference below

from dataclasses import (
    dataclass,
)  # => @dataclass(frozen=True) builds the immutable PList node


@dataclass(
    frozen=True
)  # => a persistent list node caching its own length -- O(1) to read
class PList:  # => the node type itself -- see the decorator above for immutability
    head: int  # => this node's own value
    tail: "PList | None"  # => the shared, untouched rest of the list
    length: int  # => cached at construction time -- never recomputed by walking


def plist_prepend(
    value: int, lst: "PList | None"
) -> PList:  # => O(1): no walk over lst needed
    previous_length = (
        lst.length if lst is not None else 0
    )  # => O(1) read of a cached field
    return PList(
        head=value, tail=lst, length=previous_length + 1
    )  # => reuses lst AS-IS


empty: PList | None = None  # => the shared empty base every version points back to
version_a = plist_prepend(1, empty)  # => version_a.length is 1
version_b = plist_prepend(
    2, version_a
)  # => version_b.length is 2, REUSING version_a untouched

# => structural sharing means version_b costs O(1) extra memory, not O(n)
print(version_a.length)  # => Output: 1
print(version_b.length)  # => Output: 2
print(version_b.tail is version_a)  # => Output: True -- structural sharing, not a copy
print(
    version_a.head
)  # => Output: 1 -- version_a itself was never touched by building version_b
