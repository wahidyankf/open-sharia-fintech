"""Example 84: Backpressure Strategies -- Buffer-All vs Keep-Latest (Hand-Rolled)."""

# => co-32: reactivex (RxPY 4.1.0) has NO built-in backpressure operators, so this example is
# => HAND-ROLLED stdlib Python -- a deterministic round-based simulation, not real threads, so
# => the comparison is reproducible on every run instead of depending on OS scheduling timing.


def simulate_buffer_all(item_count: int, consumer_period: int) -> tuple[list[int], int]:
    """A fast producer's items all queue up; the consumer drains them, oldest first, eventually."""
    buffer: list[int] = []  # => buffer: unbounded FIFO -- grows without limit while the producer outpaces the consumer
    consumed: list[int] = []  # => consumed: items the slow consumer has actually pulled out, in order
    peak_size = 0  # => peak_size: the largest the buffer ever got -- the MEMORY COST of this strategy
    for tick in range(item_count):  # => tick: one discrete round; the producer emits exactly one item per round
        buffer.append(tick)  # => the producer NEVER blocks and NEVER drops -- it just appends
        peak_size = max(peak_size, len(buffer))  # => track the worst-case backlog size seen so far
        if (tick + 1) % consumer_period == 0 and buffer:  # => the consumer only gets a turn every `consumer_period` ticks
            consumed.append(buffer.pop(0))  # => pop(0): FIFO order -- oldest unconsumed item first
    consumed.extend(buffer)  # => once production stops, drain whatever backlog remains -- nothing is ever lost
    return consumed, peak_size  # => (all items, in order) plus how large the backlog grew


def simulate_latest_only(item_count: int, consumer_period: int) -> tuple[list[int], int]:
    """The producer overwrites a single slot; only the newest value survives until the consumer reads it."""
    slot: int | None = None  # => slot: capacity of exactly ONE -- the opposite extreme from buffer-all
    consumed: list[int] = []  # => consumed: items the consumer actually saw (far fewer than item_count)
    dropped = 0  # => dropped: how many produced values were overwritten before anyone read them
    for tick in range(item_count):  # => tick: same discrete-round production schedule as buffer_all
        if slot is not None:  # => a previous value is still sitting there, unread
            dropped += 1  # => it's about to be clobbered -- that's a PERMANENT loss, not a delay
        slot = tick  # => the producer OVERWRITES the slot -- O(1) memory, but stale data silently disappears
        if (tick + 1) % consumer_period == 0:  # => same slow consumer cadence as buffer_all -- slot is always filled here
            consumed.append(slot)  # => the consumer reads whatever happens to be in the slot RIGHT NOW
            slot = None  # => the slot is now empty until the next produced value fills it
    if slot is not None:  # => one final value may still be sitting in the slot after production ends
        consumed.append(slot)  # => drain it so the very last emission isn't silently discarded too
    return consumed, dropped  # => (far fewer items, in order) plus how many were permanently lost


ITEM_COUNT = 9  # => how many items the fast producer emits across the simulated run
CONSUMER_PERIOD = 3  # => the slow consumer only gets to pull once every 3 rounds


if __name__ == "__main__":  # => module entry point
    buffer_all_consumed, buffer_all_peak = simulate_buffer_all(ITEM_COUNT, CONSUMER_PERIOD)
    print(f"buffer_all: consumed={buffer_all_consumed} peak={buffer_all_peak}")  # => Output: consumed=[0..8] peak=7

    latest_consumed, latest_dropped = simulate_latest_only(ITEM_COUNT, CONSUMER_PERIOD)
    print(f"latest_only: consumed={latest_consumed} dropped={latest_dropped}")  # => Output: consumed=[2,5,8] dropped=6

    # => The two strategies trade off DIFFERENT resources for the SAME root problem: a producer
    # => faster than its consumer. `buffer` keeps EVERY item (nothing is lost) at the cost of
    # => unbounded memory that grows with the speed mismatch -- fine for a short burst, dangerous
    # => for a sustained one. `latest` keeps CONSTANT memory (one slot) by cheerfully discarding
    # => every value that arrives before the previous one was read -- fine for a live price ticker
    # => where only the newest number matters, wrong for anything that must process every event
    # => (an audit log, a payment queue). Neither is "correct" in the abstract; the choice depends
    # => entirely on whether staleness or data loss is the worse failure mode for the use case.
    assert buffer_all_consumed == list(range(ITEM_COUNT))  # => buffer-all: every item eventually arrives, in order
    assert buffer_all_peak == 7  # => the backlog grew to 7 items before draining -- the memory cost, made visible
    assert latest_consumed == [2, 5, 8]  # => latest-only: the consumer only ever sees what was freshest at read time
    assert latest_dropped == 6  # => 6 of the 9 produced values were overwritten and permanently lost
    print("ex-84 OK")  # => Output: ex-84 OK
