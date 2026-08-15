# => Initialize or update deterministic state used by this demonstration.
cache: dict[str, str] = {}
# => Initialize or update deterministic state used by this demonstration.
store = {"code": "https://example.test/long"}


# => Isolate the operation so its observable behavior can be checked.
def get(key: str) -> str:
    # A cache hit avoids the durable lookup.
    # => Choose the branch that models this design condition.
    if key in cache:
        # => Return the observable result of this modeled operation.
        return cache[key]
    # A miss loads the authoritative value before populating the cache.
    # => Initialize or update deterministic state used by this demonstration.
    value = store[key]
    # => Initialize or update deterministic state used by this demonstration.
    cache[key] = value
    # => Return the observable result of this modeled operation.
    return value


# => Check the promised observable behavior of the demonstration.
assert get("code") == "https://example.test/long"
# The second read proves that the miss path populated the cache.
# => Check the promised observable behavior of the demonstration.
assert "code" in cache and get("code") == cache["code"]
# => Emit the final observable state for a direct run.
print(cache)
