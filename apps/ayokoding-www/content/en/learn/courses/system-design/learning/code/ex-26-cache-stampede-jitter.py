from random import Random


def deadlines(count: int, ttl: int, jitter: int) -> list[int]:
    # A seeded generator keeps this instructional schedule reproducible.
    random = Random(7)
    # Each entry gets a bounded offset instead of one shared deadline.
    return [ttl + random.randint(-jitter, jitter) for _ in range(count)]


result = deadlines(20, 60, 5)
# More than one deadline proves refreshes are not perfectly synchronized.
assert len(set(result)) > 1 and all(55 <= deadline <= 65 for deadline in result)
print(result)
