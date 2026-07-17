"""Example 17: Count Words Sharing a Prefix, via a Trie's Subtree Count."""

# Extending Example 16's trie (co-13): give every node a running count of how
# many WORDS pass through it. Counting prefix matches then costs exactly
# O(len(prefix)) -- walk to the prefix's node and read its count directly.
from __future__ import annotations


class CountingTrieNode:  # => a trie node that also tracks words passing through it
    def __init__(self) -> None:
        self.children: dict[str, CountingTrieNode] = {}  # => char -> child node
        self.words_through: int = 0  # => how many inserted words pass through here
        self.is_word_end: bool = False  # => True if a word ends exactly at this node


class CountingTrie:  # => a trie augmented for O(len(prefix)) prefix counting
    def __init__(self) -> None:
        self.root = CountingTrieNode()  # => an empty root

    def insert(self, word: str) -> None:  # => O(len(word)): inserts, updating counts
        node = self.root  # => starts at the root
        node.words_through += 1  # => the root itself is a "prefix" of every word
        for ch in word:  # => walks (or creates) one node per character
            if ch not in node.children:  # => this branch doesn't exist yet
                node.children[ch] = CountingTrieNode()  # => creates a fresh branch
            node = node.children[ch]  # => descends into that character's node
            node.words_through += 1  # => this node lies on the path of the new word
        node.is_word_end = True  # => marks the final node as a complete word

    def count_with_prefix(
        self, prefix: str
    ) -> int:  # => O(len(prefix)): how many inserted words start with prefix
        node = self.root  # => starts at the root
        for ch in prefix:  # => walks exactly len(prefix) hops
            if ch not in node.children:  # => the prefix path doesn't exist at all
                return 0  # => no inserted word can share this prefix
            node = node.children[ch]  # => follows the existing branch
        return node.words_through  # => the count accumulated along this exact path


trie = CountingTrie()  # => an empty counting trie
for w in [
    "cat",
    "car",
    "card",
    "care",
    "careful",
    "dog",
]:  # => a small word dictionary
    trie.insert(w)  # => O(len(w)) per insert, updating every node on the path

print(trie.count_with_prefix("car"))  # => Output: 4 -- car, card, care, careful
print(trie.count_with_prefix("care"))  # => Output: 2 -- care, careful
print(trie.count_with_prefix("dog"))  # => Output: 1
print(trie.count_with_prefix("bird"))  # => Output: 0 -- no matching prefix at all

assert trie.count_with_prefix("car") == 4  # => confirms all four "car*" words counted
assert trie.count_with_prefix("care") == 2  # => confirms the narrower prefix's count
assert trie.count_with_prefix("bird") == 0  # => confirms an absent prefix counts zero
assert trie.count_with_prefix("") == 6  # => the empty prefix matches every word
print("ex-17 OK")  # => Output: ex-17 OK
