"""Example 68: OO Behind a Functional Facade."""


class _MutableCache:  # => an OO subsystem: private, mutable state, hidden with a leading underscore
    def __init__(self) -> None:  # => constructor seeds both pieces of private mutable state
        self._store: dict[str, int] = {}  # => mutable internal state -- normal OO territory
        self._hits = 0  # => more internal, mutable bookkeeping

    def get_or_compute(self, key: str, compute: int) -> int:  # => internal OO method, DOES mutate
        if key in self._store:  # => cache hit: skip recomputation entirely
            self._hits += 1  # => internal mutation
            return self._store[key]  # => the ORIGINAL cached value, not the freshly-passed compute argument
        self._store[key] = compute  # => internal mutation
        return compute  # => first call for this key: store and return the given value


_cache = _MutableCache()  # => module-private instance -- callers never see this OO object directly


def memoized_lookup(key: str, compute: int) -> int:  # => the PURE-LOOKING FACADE callers actually use
    return _cache.get_or_compute(key, compute)  # => delegates to the OO subsystem, hides it completely
    # => from the outside, this looks like a plain function: call it, get a value back -- no exposed state


first = memoized_lookup("a", 100)  # => first call for key "a": computes and stores
second = memoized_lookup("a", 999)  # => second call, SAME key, DIFFERENT compute argument
print(first, second)  # => second call returns the CACHED 100, not 999 -- proves the facade has memory
# => Output: 100 100

facade_attrs = [attr for attr in dir(memoized_lookup) if not attr.startswith("__")]  # => inspect the facade itself
print("_store" in facade_attrs, "_hits" in facade_attrs)  # => the function object exposes no OO internals at all
# => Output: False False
