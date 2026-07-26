"""Example 13: Pin Count Guards Against Eviction -- a pinned frame is never a victim."""

from dataclasses import dataclass  # => a plain, typed record for one buffer-pool frame


@dataclass  # => auto-generates __init__ from the fields below
class Frame:  # => a buffer-pool frame that tracks how many callers currently need it
    page_id: int  # => which on-disk page this frame currently holds
    pin_count: int = 0  # => how many active readers/writers currently need this page


class PinnedFrameError(Exception):  # => raised instead of silently evicting in-use data
    """Raised when eviction is attempted on a frame with pin_count > 0."""  # => documents the contract


def pin(
    frame: Frame,
) -> None:  # => a caller starting work on the page increments the pin count
    frame.pin_count += (
        1  # => one more caller now depends on this frame staying resident
    )


def unpin(frame: Frame) -> None:  # => a caller finishing work decrements it back down
    frame.pin_count -= (
        1  # => one fewer caller depends on it -- may reach zero and become evictable
    )


def evict(
    frames: list[Frame], victim_id: int
) -> None:  # => removes a frame, but only if it is safe to
    victim = next(
        f for f in frames if f.page_id == victim_id
    )  # => locate the requested frame
    if victim.pin_count > 0:  # => the guard: refuse to evict anything still in use
        raise PinnedFrameError(
            f"page {victim_id} is pinned ({victim.pin_count} pins)"
        )  # => refuse
    frames.remove(victim)  # => only reached once pin_count is exactly zero


frames = [
    Frame(page_id=1),
    Frame(page_id=2),
]  # => two candidate frames, neither pinned yet
pin(frames[0])  # => page 1 is now in active use
raised = False  # => flips to True only if the guard actually fires below
try:  # => the guard should raise here, not silently succeed
    evict(frames, victim_id=1)  # => attempting to evict a PINNED page
except PinnedFrameError:  # => the exact exception the guard raises
    raised = True  # => confirms the guard fired instead of evicting in-use data
assert raised  # => eviction was refused while the pin was held
evict(frames, victim_id=2)  # => page 2 has zero pins -- this succeeds
assert [f.page_id for f in frames] == [
    1
]  # => only the unpinned page was actually removed
# => the pin count, not any eviction-policy ranking, had the final say over what got removed
print("ex-13 OK")  # => Output: ex-13 OK
