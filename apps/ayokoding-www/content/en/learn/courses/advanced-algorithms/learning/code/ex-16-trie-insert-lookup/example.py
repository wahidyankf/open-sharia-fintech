"""Example 16: A Prefix Trie -- Insert and Lookup in O(key-length)."""

# A trie (co-13) stores strings character by character down a tree of nodes;
# a lookup only ever walks as many nodes as the KEY IS LONG, regardless of how
# many other words share the trie -- unlike a hash set, cost never depends on n.
from __future__ import annotations


class TrieNode:  # => one node per character position along some inserted word
    def __init__(self) -> None:
        self.children: dict[str, TrieNode] = {}  # => char -> the next node down
        self.is_word_end: bool = False  # => True if a word ends exactly at this node


class Trie:  # => the trie itself -- just a reference to its root node
    def __init__(self) -> None:
        self.root = TrieNode()  # => an empty root with no children yet

    def insert(self, word: str) -> None:  # => O(len(word)): adds one word to the trie
        node = self.root  # => starts walking from the root
        for ch in word:  # => one hop per character
            if ch not in node.children:  # => this character hasn't been seen at this
                # => depth before -- create a fresh branch for it
                node.children[ch] = TrieNode()  # => a brand-new node for this branch
            node = node.children[ch]  # => descends into that character's node
        node.is_word_end = True  # => marks the LAST node visited as a word boundary

    def search(self, word: str) -> bool:  # => O(len(word)): True only for a full word
        node = self.root  # => starts walking from the root
        for ch in word:  # => walks exactly len(word) hops -- never more, never fewer
            if ch not in node.children:  # => the path doesn't exist -- word is absent
                return False  # => no need to walk further
            node = node.children[ch]  # => follows the existing branch
        return node.is_word_end  # => True only if THIS exact word was inserted


trie = Trie()  # => an empty trie
for w in ["cat", "car", "card", "care", "dog"]:  # => five words sharing prefixes
    trie.insert(w)  # => O(len(w)) per insert

print(trie.search("car"))  # => Output: True -- "car" was inserted exactly
print(trie.search("ca"))  # => Output: False -- "ca" is a prefix, not a full word
print(trie.search("care"))  # => Output: True
print(trie.search("caring"))  # => Output: False -- never inserted

assert trie.search("car") is True  # => confirms a full inserted word is found
assert trie.search("ca") is False  # => confirms a mere PREFIX is not a match
assert trie.search("dog") is True  # => confirms an unrelated word is found too
assert trie.search("do") is False  # => confirms partial prefixes never match
print("ex-16 OK")  # => Output: ex-16 OK
