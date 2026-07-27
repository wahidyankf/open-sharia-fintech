"""Example 3: pytest verification for Slot Array Append."""

from example import HEADER_SIZE, SLOT_SIZE, append_slot, header, new_page


def test_first_append_advances_pd_lower_by_slot_size() -> None:
    page = new_page()
    before, _ = header(page)
    after = append_slot(page, offset=100, length=10)
    assert after == before + SLOT_SIZE  # => exactly one slot's worth of growth


def test_three_appends_grow_pd_lower_by_three_slots() -> None:
    page = new_page()
    before, _ = header(page)
    after = before
    for _ in range(3):
        after = append_slot(page, offset=200, length=5)
    assert (
        after == before + 3 * SLOT_SIZE
    )  # => three appends -> three slots' worth of growth
    assert (
        after - HEADER_SIZE
    ) // SLOT_SIZE == 3  # => slot count derived from pd_lower matches


# => Run: pytest -- Output: 2 passed
