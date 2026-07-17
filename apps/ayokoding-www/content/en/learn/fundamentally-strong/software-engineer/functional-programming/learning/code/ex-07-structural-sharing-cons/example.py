"""Example 7: A Persistent Cons-List Prepend."""

from __future__ import (
    annotations,
)  # => lets ConsList reference itself in its own field type

from dataclasses import (
    dataclass,
)  # => @dataclass generates __init__/__repr__/__eq__ for the node


@dataclass(frozen=True)  # => frozen: once linked, a node's head/tail never change
class ConsList:  # => the classic persistent linked list: a head value plus a tail list
    head: int  # => this node's own value
    tail: "ConsList | None"  # => None marks the empty tail -- the end of the list


def prepend(value: int, lst: "ConsList | None") -> ConsList:  # => builds a NEW node
    return ConsList(
        head=value, tail=lst
    )  # => tail is the OLD list, reused, never copied


def to_list(
    lst: "ConsList | None",
) -> list[int]:  # => walks nodes into a plain list, for printing
    result: list[int] = []  # => the plain list this walk accumulates into
    while lst is not None:  # => walking SHARED structure -- no mutation happens here
        result.append(lst.head)  # => reads this node's value
        lst = lst.tail  # => advances to the next shared node, never rewriting it
    return (
        result  # => a fresh plain list -- the ConsList nodes themselves stay untouched
    )


empty: ConsList | None = (
    None  # => the empty list -- the shared base every version points to
)
version_a = prepend(1, empty)  # => version_a is [1]
version_b = prepend(
    2, version_a
)  # => version_b is [2, 1] -- REUSES version_a as its tail

print(to_list(version_a))  # => Output: [1]
print(to_list(version_b))  # => Output: [2, 1]
print(version_b.tail is version_a)  # => Output: True -- structural sharing, not a copy
