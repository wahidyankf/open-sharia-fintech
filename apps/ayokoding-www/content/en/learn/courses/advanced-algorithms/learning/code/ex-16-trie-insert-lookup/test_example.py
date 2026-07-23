"""Example 16: pytest verification for Trie Insert and Lookup."""

from example import Trie


def test_hit_on_exact_inserted_word() -> None:
    trie = Trie()
    trie.insert("hello")
    assert trie.search("hello") is True  # => an exact match is found


def test_miss_on_prefix_that_was_never_a_full_word() -> None:
    trie = Trie()
    trie.insert("hello")
    assert trie.search("hell") is False  # => a prefix alone is not a stored word


def test_miss_on_completely_absent_word() -> None:
    trie = Trie()
    trie.insert("hello")
    assert trie.search("world") is False  # => an unrelated word is never found


# => Run: pytest -- Output: 3 passed
