"""Example 44: pytest verification for a Weak-Value Identity Map."""

import gc
import weakref

from example import User


def test_entry_present_while_strong_reference_exists() -> None:
    cache: weakref.WeakValueDictionary[int, User] = weakref.WeakValueDictionary()  # => a fresh weak map
    user = User(id=9, name="Grace")  # => a strong reference held by this local variable
    cache[9] = user  # => weakly referenced by the map
    assert cache[9] is user  # => present and correct while `user` is alive


def test_entry_disappears_after_the_last_strong_reference_drops() -> None:
    cache: weakref.WeakValueDictionary[int, User] = weakref.WeakValueDictionary()
    cache[1] = User(id=1, name="Temp")  # => NO local variable holds a strong reference at all
    gc.collect()  # => forces collection so the drop is deterministic here too
    assert 1 not in cache  # => nothing kept the object alive past this statement


# => Run: pytest -- Output: 2 passed
