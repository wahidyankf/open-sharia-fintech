"""Example 8: pytest verification for In-Page Compaction."""

from example import compact, delete, header, insert, new_page, read


def test_surviving_slot_resolves_after_compaction() -> None:
    page = new_page()
    a = insert(page, b"keep-a")
    b = insert(page, b"delete-me")
    delete(page, b)
    compact(page)
    assert (
        read(page, a) == b"keep-a"
    )  # => slot a's offset was rewritten but its bytes stayed correct


def test_compaction_reclaims_the_deleted_gap() -> None:
    page = new_page()
    insert(page, b"keep-a")
    b = insert(page, b"delete-me")
    delete(page, b)
    compact(page)
    _, pd_upper = header(page)
    assert pd_upper == 4096 - len(
        b"keep-a"
    )  # => only the surviving record's bytes remain reserved


# => Run: pytest -- Output: 2 passed
