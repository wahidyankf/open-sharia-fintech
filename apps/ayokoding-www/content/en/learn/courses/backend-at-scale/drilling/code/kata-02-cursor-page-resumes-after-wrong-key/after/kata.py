# pyright: strict
"""Kata 2 (after): cursor pagination resumes AFTER the last-seen id (keyset)."""

ROWS = list(range(1, 11))  # => ids 1..10


def page_starting_after(starting_after: int | None, limit: int) -> list[int]:
    threshold = 0 if starting_after is None else starting_after
    # THE FIX: a cursor is a KEY -- resume with WHERE id > cursor, not a row offset.
    return [r for r in ROWS if r > threshold][:limit]


first = page_starting_after(None, 3)
second = page_starting_after(3, 3)  # resume after id 3 -> [4, 5, 6]
print(f"page 1: {first}")  # [1, 2, 3]
print(f"page 2 (starting_after=3): {second}")  # [4, 5, 6] -- correct keyset resume
assert second == [4, 5, 6]
# Non-contiguous ids are handled correctly by the keyset WHERE, unlike an offset.
SPARSE = [1, 2, 7, 9, 20]
page = [r for r in SPARSE if r > 7][:2]
print(f"sparse keyset page after 7: {page}")  # [9, 20]
assert page == [9, 20]
