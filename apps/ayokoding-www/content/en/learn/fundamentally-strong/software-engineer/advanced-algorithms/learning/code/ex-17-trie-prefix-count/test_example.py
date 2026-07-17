"""Example 17: pytest verification for Trie Prefix Counting."""

from example import CountingTrie


def test_prefix_count_matches_manual_count() -> None:
    trie = CountingTrie()
    words = ["ant", "anthem", "ants", "bee"]
    for w in words:
        trie.insert(w)
    expected = sum(1 for w in words if w.startswith("ant"))  # => 3
    assert trie.count_with_prefix("ant") == expected


def test_absent_prefix_returns_zero() -> None:
    trie = CountingTrie()
    trie.insert("hello")
    assert trie.count_with_prefix("xyz") == 0  # => no word starts this way


# => Run: pytest -- Output: 2 passed
