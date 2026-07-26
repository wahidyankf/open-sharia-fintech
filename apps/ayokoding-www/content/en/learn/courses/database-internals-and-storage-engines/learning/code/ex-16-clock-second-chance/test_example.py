"""Example 16: pytest verification for CLOCK (Second-Chance) Eviction."""

from example import Frame, clock_evict


def test_unreferenced_frame_is_evicted_first() -> None:
    frames = [
        Frame(page_id=1, referenced=True),
        Frame(page_id=2),
        Frame(page_id=3, referenced=True),
    ]
    victim, _ = clock_evict(frames, hand=0)
    assert victim == 2


def test_referenced_frame_gets_its_bit_cleared_not_evicted() -> None:
    frames = [
        Frame(page_id=1, referenced=True),
        Frame(page_id=2),
        Frame(page_id=3, referenced=True),
    ]
    clock_evict(frames, hand=0)
    survivor = next(f for f in frames if f.page_id == 1)
    assert (
        survivor.referenced is False
    )  # => it survived, but its second chance is now spent


# => Run: pytest -- Output: 2 passed
