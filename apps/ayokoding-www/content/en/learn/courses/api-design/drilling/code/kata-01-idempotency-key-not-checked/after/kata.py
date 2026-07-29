# pyright: strict
"""Kata 1 (after): the Idempotency-Key is looked up before creating anything."""

STORE: dict[int, dict[str, object]] = {}
IDEMPOTENCY_STORE: dict[str, dict[str, object]] = {}
NEXT_ID = [1]


def create_article(idempotency_key: str, title: str) -> dict[str, object]:
    # THE FIX: check IDEMPOTENCY_STORE first -- a known key returns the
    # ORIGINAL response instead of creating a second article.
    if idempotency_key in IDEMPOTENCY_STORE:
        return IDEMPOTENCY_STORE[idempotency_key]
    new_id = NEXT_ID[0]
    article: dict[str, object] = {"id": new_id, "title": title}
    STORE[new_id] = article
    IDEMPOTENCY_STORE[idempotency_key] = article
    NEXT_ID[0] += 1
    return article


first = create_article("retry-key-1", "Launch Announcement")
print(f"first call: {first}")

replay = create_article("retry-key-1", "Launch Announcement")
print(f"replay call (same key): {replay}")

print(f"total articles created: {len(STORE)}")
