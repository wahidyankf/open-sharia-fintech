"""Example 79: Prefix Trie with Dict-Based Children."""


class TrieNode:
    # Each node's children is a dict mapping char -> next TrieNode -- a specialized
    # tree where the PATH from the root spells out a string (co-08, co-10).
    def __init__(self) -> None:  # => constructor
        self.children: dict[
            str, "TrieNode"
        ] = {}  # => O(1) average lookup per character
        self.is_word_end = False  # => marks "a complete word ends exactly here"


class Trie:
    def __init__(self) -> None:  # => constructor
        self.root = TrieNode()  # => the empty-prefix starting point for every word

    # Walks/creates one node per character -- O(len(word)), independent of trie size.
    def insert(self, word: str) -> None:  # => builds the branch for word if missing
        node = self.root  # => starts descending from the root
        for char in word:  # => descends one level per character
            if (
                char not in node.children
            ):  # => O(1) average -- create the branch if missing
                node.children[char] = TrieNode()  # => a fresh, empty branch for char
            node = node.children[char]  # => descend into the (now-guaranteed) child
        node.is_word_end = (
            True  # => marks the END of this exact word, not just a prefix
        )

    # True only if word was inserted as a COMPLETE word, not merely a prefix of one.
    def search(self, word: str) -> bool:  # => a full-word membership check
        node = self._find_node(word)  # => walks as far as word's characters allow
        return (
            node is not None and node.is_word_end
        )  # => must reach the exact word-end flag

    # True if ANY inserted word begins with prefix -- word-end flag not required.
    def starts_with(self, prefix: str) -> bool:  # => a prefix-only membership check
        return (
            self._find_node(prefix) is not None
        )  # => reaching the node at all is enough

    def _find_node(self, text: str) -> TrieNode | None:  # => shared descent helper
        node = self.root  # => starts descending from the root
        for char in text:  # => O(len(text)) descent, following existing branches only
            if char not in node.children:  # => the path breaks here
                return None  # => text is not a prefix of anything stored
            node = node.children[char]  # => keep descending along the existing branch
        return node  # => the node reached after consuming all of text


trie = Trie()  # => an empty trie to start
for word in ("cat", "car", "card"):  # => builds a trie sharing the "ca" prefix
    trie.insert(word)  # => inserts each word one character-path at a time

found_word = trie.search("car")  # => "car" was inserted as a complete word
missing_word = trie.search(
    "ca"
)  # => "ca" is only a PREFIX, never inserted as a whole word
valid_prefix = trie.starts_with("ca")  # => "ca" IS a prefix of cat, car, and card
print(found_word)  # => Output: True
print(missing_word)  # => Output: False
print(valid_prefix)  # => Output: True

assert found_word is True  # => confirms an inserted complete word is found
assert (
    missing_word is False
)  # => confirms a prefix-only string is NOT reported as a word
assert (
    valid_prefix is True
)  # => confirms prefix matching succeeds independent of word-end
print("ex-79 OK")  # => Output: ex-79 OK
