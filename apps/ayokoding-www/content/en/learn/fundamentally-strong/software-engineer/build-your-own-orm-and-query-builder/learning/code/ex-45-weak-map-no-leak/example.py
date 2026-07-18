"""Example 45: A Weak Identity Map Shrinks Under GC Instead of Leaking."""  # => this concept

import dataclasses  # => the loaded domain objects
import gc  # => forces a collection cycle so this example is deterministic
import weakref  # => co-14: the same WeakValueDictionary mechanism as Example 44, at scale


@dataclasses.dataclass  # => a loaded domain object
class User:  # => held only weakly by the cache below
    id: int  # => primary key
    name: str  # => an ordinary column


def fill_cache(cache: weakref.WeakValueDictionary[int, User], count: int) -> list[User]:  # => co-14 helper
    users = [User(id=i, name=f"user-{i}") for i in range(count)]  # => `count` STRONG references, in a list
    for u in users:  # => `u` is LOCAL to this function -- it does not leak into the caller's scope
        cache[u.id] = u  # => each cached weakly -- the LIST is what keeps them alive, not the cache
    return users  # => the caller now holds the ONLY strong references, via this returned list


cache: weakref.WeakValueDictionary[int, User] = weakref.WeakValueDictionary()  # => co-14: the weak map
loaded_users = fill_cache(cache, 100)  # => loads 100 rows, simulating a session that touched 100 objects
assert len(cache) == 100  # => every one of the 100 objects is currently alive and cached

loaded_users = loaded_users[:10]  # => drops the STRONG references to 90 of the 100 objects
gc.collect()  # => forces collection so the shrink is deterministic in this example
assert len(cache) == 10  # => co-14: exactly the 10 still strongly-referenced objects remain cached
print(len(cache))  # => Output: 10
