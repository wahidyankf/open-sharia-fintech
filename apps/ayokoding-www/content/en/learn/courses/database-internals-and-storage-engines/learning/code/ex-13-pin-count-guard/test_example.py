"""Example 13: pytest verification for the Pin Count Guard."""

import pytest

from example import Frame, PinnedFrameError, evict, pin, unpin


def test_pinned_frame_cannot_be_evicted() -> None:
    frames = [Frame(page_id=1)]
    pin(frames[0])
    with pytest.raises(PinnedFrameError):
        evict(frames, victim_id=1)


def test_unpinned_frame_can_be_evicted() -> None:
    frames = [Frame(page_id=1)]
    pin(frames[0])
    unpin(frames[0])  # => pin_count is back to zero
    evict(frames, victim_id=1)
    assert frames == []


# => Run: pytest -- Output: 2 passed
