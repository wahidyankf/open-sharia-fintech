"""Example 45: pytest verification for a Weak Map Shrinking Under GC."""

import gc
import weakref

from example import User, fill_cache


def test_cache_size_matches_live_strong_references() -> None:
    cache: weakref.WeakValueDictionary[int, User] = weakref.WeakValueDictionary()  # => a fresh weak map
    live = fill_cache(cache, 20)  # => 20 strongly-referenced objects, all cached weakly
    assert len(cache) == 20  # => all 20 alive and cached
    assert len(live) == 20  # => the returned list is what's keeping them alive


def test_dropping_all_strong_references_empties_the_cache() -> None:
    cache: weakref.WeakValueDictionary[int, User] = weakref.WeakValueDictionary()  # => a fresh weak map
    live = fill_cache(cache, 5)  # => 5 strongly-referenced objects
    live: list[User] = []  # => drops every strong reference in one assignment, type kept explicit
    gc.collect()  # => deterministic collection for the test
    assert len(live) == 0  # => confirms the reassignment took effect
    assert len(cache) == 0  # => the cache tracks the live set exactly, down to zero


# => Run: pytest -- Output: 2 passed
