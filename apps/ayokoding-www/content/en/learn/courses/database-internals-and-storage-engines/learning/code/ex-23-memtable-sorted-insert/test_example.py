"""Example 23: pytest verification for Memtable Sorted Insert."""

from example import memtable, memtable_put


def test_memtable_iterates_in_sorted_key_order() -> None:
    memtable.clear()
    for k, v in [("z", "26"), ("a", "1"), ("m", "13")]:
        memtable_put(k, v)
    assert [k for k, _ in memtable] == ["a", "m", "z"]


def test_put_on_existing_key_overwrites_in_place() -> None:
    memtable.clear()
    memtable_put("a", "1")
    memtable_put("a", "one")
    assert memtable == [
        ("a", "one")
    ]  # => no duplicate entry -- the value was updated, not appended


# => Run: pytest -- Output: 2 passed
