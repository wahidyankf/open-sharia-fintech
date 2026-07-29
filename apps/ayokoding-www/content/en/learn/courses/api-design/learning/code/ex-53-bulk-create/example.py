# pyright: strict
"""Example 53: Bulk-Creating Many Resources in One Request. (co-32)

A single POST carrying a LIST of resources creates all of them in one round
trip -- distinct from Example 52's mixed-operation batch, this is N creates
of the SAME kind, verified by an id assigned per created item.
"""

STORE: dict[int, dict[str, str]] = {}  # => the resource store bulk-create writes into
NEXT_ID = [1]  # => a mutable counter cell -- mints a fresh id per created item


def bulk_create_articles(titles: list[str]) -> list[dict[str, object]]:  # => POST /articles/bulk
    created: list[dict[str, object]] = []  # => co-32: one created record per input title
    for title in titles:  # => co-32: iterates the WHOLE input list in one call
        new_id = NEXT_ID[0]  # => a fresh id for this specific item
        STORE[new_id] = {"title": title}  # => writes it into the store
        NEXT_ID[0] += 1  # => advances the counter for the NEXT item
        created.append({"id": new_id, "title": title})  # => co-32: records what was actually created
    return created  # => the full list of created resources, one per input title


input_titles = ["First", "Second", "Third"]  # => three titles submitted in ONE request
created = bulk_create_articles(input_titles)  # => co-32: creates all three in a single call
# => created has 3 dicts, ids 1, 2, 3 -- one HTTP round trip produced three resources
print(f"created {len(created)} articles: {created}")  # => Output: 3 articles, each with its own id

assert len(created) == len(input_titles)  # => co-32: verifies created count matches input count exactly
assert {c["id"] for c in created} == {1, 2, 3}  # => co-32: verifies each got a DISTINCT id
