"""Example 41: LRU-K vs Plain LRU on a Scan-Then-Hot Pattern."""
# LRU-K (co-05) ranks a page by its K-th most recent access, not just its latest one.

from collections import (
    OrderedDict,
)  # => stdlib ordered-dict, gives free "most-recently-touched" order

CAPACITY = 3  # => the buffer pool holds at most 3 frames in this example


def simulate_lru(
    accesses: list[str], capacity: int
) -> list[str]:  # => plain LRU eviction
    cache: OrderedDict[str, None] = (
        OrderedDict()
    )  # => key order IS recency order -- newest at the end
    for page in accesses:  # => walk the access trace in order
        if page in cache:  # => a hit -- refresh its recency
            cache.move_to_end(page)  # => moves it to the "most recently used" end
        else:  # => a miss -- must load the page
            if len(cache) >= capacity:  # => pool is full -- must evict first
                cache.popitem(
                    last=False
                )  # => evicts the LEAST recently used page (the front)
            cache[page] = None  # => insert as most recently used
    return list(cache.keys())  # => final resident set, in recency order


def simulate_lru_k(
    accesses: list[str], capacity: int, k: int
) -> list[str]:  # => LRU-K eviction
    cache: dict[
        str, None
    ] = {}  # => the resident set -- insertion order tracked by dict semantics
    history: dict[
        str, list[int]
    ] = {}  # => page -> its last k access timestamps, oldest first
    for t, page in enumerate(
        accesses, start=1
    ):  # => t is a monotonic logical timestamp
        hist = history.setdefault(page, [])  # => this page's access-time history so far
        hist.append(t)  # => record this access
        if (
            len(hist) > k
        ):  # => only the last K references matter for the K-distance rule
            hist.pop(0)  # => drop the oldest, keep exactly K entries
        if (
            page not in cache and len(cache) >= capacity
        ):  # => a miss into a full pool -- must evict

            def backward_k_distance(
                candidate: str,
            ) -> float:  # => how "cold" a page looks to LRU-K
                h = history[
                    candidate
                ]  # => that candidate page's own access-time history
                if (
                    len(h) < k
                ):  # => fewer than K references ever seen -- treat as infinitely cold
                    return float(
                        "inf"
                    )  # => a page seen once during a scan looks maximally evictable
                return t - h[0]  # => distance back to the K-th most recent reference

            victim = max(
                cache, key=lambda p: (backward_k_distance(p), -history[p][-1])
            )  # => coldest wins
            del cache[
                victim
            ]  # => evict whichever page looks coldest under the K-distance rule
        cache[page] = None  # => insert (or refresh) this page as resident
    return list(
        cache.keys()
    )  # => final resident set, insertion order (hot inserted once, never evicted)


accesses = [
    "hot",
    "hot",
    "p1",
    "p2",
    "p3",
    "p4",
    "p5",
]  # => hot touched twice, then a long distinct scan
lru_result = simulate_lru(accesses, CAPACITY)  # => run the trace through plain LRU
lru_k_result = simulate_lru_k(
    accesses, CAPACITY, k=2
)  # => and through LRU-K, for comparison
print(lru_result)  # => Output: ['p3', 'p4', 'p5']
print(lru_k_result)  # => Output: ['hot', 'p4', 'p5']

assert (
    "hot" not in lru_result
)  # => plain LRU evicted the hot page during the one-off scan
assert "hot" in lru_k_result  # => LRU-K correctly kept the hot page resident
print("ex-41 OK")  # => Output: ex-41 OK
