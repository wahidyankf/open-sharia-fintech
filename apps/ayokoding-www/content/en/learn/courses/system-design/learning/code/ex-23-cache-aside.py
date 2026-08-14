cache: dict[str, str] = {}
store = {"code": "https://example.test/long"}


def get(key: str) -> str:
    # A cache hit avoids the durable lookup.
    if key in cache:
        return cache[key]
    # A miss loads the authoritative value before populating the cache.
    value = store[key]
    cache[key] = value
    return value


assert get("code") == "https://example.test/long"
# The second read proves that the miss path populated the cache.
assert "code" in cache and get("code") == cache["code"]
print(cache)
