"""Example 44: Back the Identity Map With a WeakValueDictionary."""  # => this concept

import dataclasses  # => the loaded domain object, held ONLY weakly by the map
import gc  # => forces a collection cycle so this example is deterministic
import weakref  # => co-14: WeakValueDictionary is the whole mechanism


@dataclasses.dataclass  # => must NOT be frozen/slotted in a way that blocks weak references
class User:  # => the type the weak identity map holds -- garbage-collectable when unreferenced
    id: int  # => primary key
    name: str  # => an ordinary column


cache: weakref.WeakValueDictionary[int, User] = weakref.WeakValueDictionary()  # => co-14: the weak map itself
user = User(id=1, name="Alice")  # => the ONLY strong reference to this object right now
cache[1] = user  # => the map holds a WEAK reference -- this line does NOT keep user alive by itself
assert 1 in cache  # => while `user` is still referenced, the entry is present
assert cache[1] is user  # => and it's the exact same object

del user  # => drops the ONLY strong reference anywhere in this program
gc.collect()  # => forces collection so the drop is deterministic in this example
assert 1 not in cache  # => co-14: the entry disappeared -- nothing kept it alive after the strong ref went
print(1 in cache)  # => Output: False
