# pyright: strict
"""Kata 1 (before): POST accepts an Idempotency-Key header but never checks it."""

STORE: dict[int, dict[str, object]] = {}
NEXT_ID = [1]


def create_article(idempotency_key: str, title: str) -> dict[str, object]:
    # THE BUG: idempotency_key is accepted as a parameter but never looked up
    # anywhere -- every call creates a new article, key or no key.
    new_id = NEXT_ID[0]
    article: dict[str, object] = {"id": new_id, "title": title}
    STORE[new_id] = article
    NEXT_ID[0] += 1
    return article


first = create_article("retry-key-1", "Launch Announcement")
print(f"first call: {first}")

replay = create_article("retry-key-1", "Launch Announcement")  # a client retry after a timeout
print(f"replay call (same key): {replay}")

print(f"total articles created: {len(STORE)}")
