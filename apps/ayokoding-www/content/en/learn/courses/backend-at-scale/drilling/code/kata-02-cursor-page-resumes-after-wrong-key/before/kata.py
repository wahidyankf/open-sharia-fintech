# pyright: strict
"""Kata 2 (before): cursor pagination resumes from the WRONG key (offset instead of after-id)."""

ROWS = list(range(1, 11))  # => ids 1..10


def page_starting_after(starting_after: int | None, limit: int) -> list[int]:
    # THE BUG: the "cursor" is treated as an OFFSET (rows[:cursor]) instead of a
    # key to resume AFTER, so the first page is truncated and paging is broken.
    if starting_after is None:
        return ROWS[:limit]  # correct only for the first page
    # BUG: slicing from the START up to starting_after, not resuming AFTER it.
    return ROWS[starting_after : starting_after + limit]  # treats cursor as an offset index


first = page_starting_after(None, 3)
second = page_starting_after(3, 3)  # intent: resume after id 3 -> [4, 5, 6]
print(f"page 1: {first}")  # OK: [1, 2, 3]
print(f"page 2 (starting_after=3): {second}")  # BUG: [4, 5, 6] only by accident here -- see offset semantics
print("page 2 intent was [4, 5, 6]; cursor-as-offset breaks when ids are non-contiguous")
