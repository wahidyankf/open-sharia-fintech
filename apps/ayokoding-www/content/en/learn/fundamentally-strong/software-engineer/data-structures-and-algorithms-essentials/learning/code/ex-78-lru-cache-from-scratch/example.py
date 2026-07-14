"""Example 78: LRU Cache from Scratch -- Dict + Doubly Linked List."""

from __future__ import (
    annotations,
)  # => enables forward references to the class defined below


class DLLNode:  # => a doubly linked node: prev AND next, for O(1) removal from anywhere (co-07)
    def __init__(self, key: int, val: int) -> None:  # => constructor
        self.key = key  # => the cache key this node represents
        self.val = val  # => the cached value for that key
        self.prev: DLLNode | None = (
            None  # => no neighbor yet -- wired in by the list ops below
        )
        self.next: DLLNode | None = (
            None  # => no neighbor yet -- wired in by the list ops below
        )


class LRUCache:
    # A dict gives O(1) key lookup; a doubly linked list gives O(1) reordering --
    # together they make BOTH get and put O(1), which neither structure alone can do (co-08, co-07).
    def __init__(self, capacity: int) -> None:  # => constructor
        self.capacity = capacity  # => the maximum number of entries this cache holds
        self.cache: dict[int, DLLNode] = {}  # => key -> node, for O(1) lookup
        self.head = DLLNode(0, 0)  # => dummy head: head.next is the MOST recently used
        self.tail = DLLNode(0, 0)  # => dummy tail: tail.prev is the LEAST recently used
        self.head.next = self.tail  # => links the two sentinels together (empty list)
        self.tail.prev = self.head  # => links the two sentinels together (empty list)

    # Unlinks node from wherever it currently sits -- O(1), no scanning required.
    def _remove(self, node: DLLNode) -> None:  # => internal doubly linked list helper
        assert (
            node.prev is not None and node.next is not None
        )  # => never called on a sentinel
        node.prev.next = node.next  # => the node before it now points past it
        node.next.prev = node.prev  # => the node after it now points back past it

    # Splices node in right after the dummy head -- marks it as most-recently-used.
    def _insert_at_front(
        self, node: DLLNode
    ) -> None:  # => internal doubly linked list helper
        node.prev = self.head  # => node's prev is now the dummy head
        node.next = (
            self.head.next
        )  # => node's next is whatever WAS right after the head
        assert (
            self.head.next is not None
        )  # => the list always has at least the dummy tail
        self.head.next.prev = node  # => the old first real node now points back at node
        self.head.next = (
            node  # => the dummy head now points at node -- node is now first
        )

    def get(self, key: int) -> int:  # => O(1) lookup + O(1) reorder
        if key not in self.cache:  # => O(1) average dict miss
            return -1  # => the sentinel value for "not found"
        node = self.cache[key]  # => the node holding this key's value
        self._remove(node)  # => touching a key makes it MOST recently used
        self._insert_at_front(node)  # => O(1): move to the front without scanning
        return node.val  # => the cached value for key

    def put(self, key: int, val: int) -> None:  # => O(1) insert/update + eviction check
        if (
            key in self.cache
        ):  # => key already present -- update and refresh its position
            self._remove(self.cache[key])  # => unlink the stale entry first
        node = DLLNode(key, val)  # => a fresh node holding the new value
        self.cache[key] = node  # => registers it in the lookup dict
        self._insert_at_front(node)  # => marks it as most-recently-used
        if (
            len(self.cache) > self.capacity
        ):  # => over capacity -- evict the LEAST recently used
            lru = self.tail.prev  # => the node right before the dummy tail
            assert (
                lru is not None and lru is not self.head
            )  # => the cache is non-empty here
            self._remove(lru)  # => unlinks the least-recently-used node
            del self.cache[lru.key]  # => O(1): drop it from the lookup dict too


cache = LRUCache(2)  # => capacity 2 -- the third distinct key forces an eviction
cache.put(1, 100)  # => cache: {1: 100} -- most-recent is 1
cache.put(2, 200)  # => cache: {1: 100, 2: 200} -- most-recent is 2
cache.get(1)  # => touches 1 -- 1 becomes most-recently-used again, 2 becomes least
cache.put(3, 300)  # => over capacity -- evicts 2 (the least recently used)
evicted = cache.get(2)  # => 2 was evicted -- lookup misses
kept = cache.get(1)  # => 1 was touched recently -- survives eviction
print(evicted, kept)  # => Output: -1 100

assert evicted == -1  # => confirms the least-recently-used key was evicted
assert kept == 100  # => confirms the recently-touched key survived
print("ex-78 OK")  # => Output: ex-78 OK
