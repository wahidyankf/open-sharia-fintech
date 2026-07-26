"""Example 16: CLOCK (Second-Chance) Eviction -- a reference bit approximates LRU cheaply."""

from dataclasses import dataclass  # => a plain, typed record for one buffer-pool frame


@dataclass  # => auto-generates __init__ from the fields below
class Frame:  # => a buffer-pool frame carrying one cheap reference bit
    page_id: int  # => which on-disk page this frame currently holds
    referenced: bool = (
        False  # => set True on every access; CLOCK's cheap stand-in for "recently used"
    )


def clock_evict(
    frames: list[Frame], hand: int
) -> tuple[int, int]:  # => returns (victim_id, new_hand)
    while True:  # => the "clock hand" sweeps frames in a circle until it finds a victim
        frame = frames[hand]  # => the frame currently under the sweeping hand
        if (
            frame.referenced
        ):  # => this frame gets a "second chance" -- clear the bit and move on
            frame.referenced = (
                False  # => second chance spent -- next sweep WOULD evict it
            )
            hand = (hand + 1) % len(
                frames
            )  # => advance the hand, wrapping around circularly
        else:  # => this frame's bit was already clear -- it becomes the victim
            victim_id = frame.page_id  # => remember which page is being evicted
            del frames[hand]  # => remove it from the pool entirely
            return victim_id, hand % max(
                len(frames), 1
            )  # => report the victim and where the hand stops next


frames = [  # => three candidate frames for the clock hand to sweep across
    Frame(page_id=1, referenced=True),  # => recently accessed
    Frame(page_id=2),  # => NOT recently accessed -- referenced defaults to False
    Frame(page_id=3, referenced=True),  # => recently accessed
]
victim, hand = clock_evict(frames, hand=0)  # => the hand starts sweeping from index 0
print(victim)  # => Output: 2
# => the hand never even had to inspect page 1 or 3's bit a second time to find this victim
print([(f.page_id, f.referenced) for f in frames])  # => Output: [(1, False), (3, True)]

assert (
    victim == 2
)  # => page 2's bit was clear -- it becomes the victim once the hand reaches it
assert (
    frames[0].referenced is False
)  # => page 1 got a SECOND CHANCE: its bit was cleared, not evicted
# => a cleared bit today means page 1 WOULD be the next victim if the hand sweeps again
print("ex-16 OK")  # => Output: ex-16 OK
