"""Example 24: pytest verification for Flushing a Memtable to an SSTable."""

from example import flush


def test_flush_returns_a_sorted_sstable() -> None:
    mt = [("c", "3"), ("a", "1"), ("b", "2")]
    sstable = flush(mt)
    assert sstable == [("a", "1"), ("b", "2"), ("c", "3")]


def test_flush_clears_the_source_memtable() -> None:
    mt = [("a", "1")]
    flush(mt)
    assert mt == []


# => Run: pytest -- Output: 2 passed
