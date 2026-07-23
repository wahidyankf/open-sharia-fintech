"""Example 87: An Annotated Marble Diagram for merge -> map -> debounce."""

from collections.abc import Callable  # => Callable: the correct typed annotation for "a function value" (not builtin callable())

# => co-30: marble diagrams visualize emissions over TIME -- each event is (tick, value). co-33:
# => this is discrete-event reactive-streams style, not continuous-time FRP. A deterministic
# => virtual-clock simulation (no real timers) keeps the diagram exactly reproducible.

MarbleEvent = tuple[int, str]  # => a single marble: (the tick it fires on, the value it carries)

SOURCE_A: list[MarbleEvent] = [(0, "a1"), (3, "a2"), (7, "a3")]  # => stream A: 3 marbles on its own timeline
SOURCE_B: list[MarbleEvent] = [(1, "b1"), (2, "b2"), (8, "b3")]  # => stream B: 3 marbles on a different timeline


def merge_marbles(a: list[MarbleEvent], b: list[MarbleEvent]) -> list[MarbleEvent]:
    """merge: interleave two timelines into one, ordered strictly by tick -- no transformation."""
    return sorted(a + b, key=lambda event: event[0])  # => sort by tick -- ties keep list-concatenation order


def map_marbles(events: list[MarbleEvent], transform: Callable[[str], str]) -> list[MarbleEvent]:
    """map: transform each marble's VALUE, leaving its TICK (its position in time) untouched."""
    return [(tick, transform(value)) for tick, value in events]  # => timing is preserved; only payload changes


def debounce_marbles(events: list[MarbleEvent], quiet: int) -> list[MarbleEvent]:
    """debounce: an event only survives if the source stays SILENT for `quiet` ticks after it."""
    result: list[MarbleEvent] = []  # => result: the settled marbles that actually make it through
    for index, (tick, value) in enumerate(events):  # => walk the timeline in order, one marble at a time
        next_tick = events[index + 1][0] if index + 1 < len(events) else None  # => when does the NEXT marble fire?
        gap = None if next_tick is None else next_tick - tick  # => the silence AFTER this marble, in ticks
        if gap is None or gap >= quiet:  # => nothing arrived soon enough to supersede this one
            result.append((tick + quiet, value))  # => it fires, but DELAYED by `quiet` ticks -- debounce's cost
    return result  # => every surviving marble is the LAST one in its burst, emitted after the burst goes quiet


def render_timeline(events: list[MarbleEvent], length: int) -> str:
    """A plain-text marble diagram: '-' means silence, else the first letter of the value at that tick."""
    frame = ["-"] * length  # => frame: one character slot per tick, all silent by default
    for tick, value in events:  # => stamp each marble's initial onto its tick position
        if 0 <= tick < length:  # => guard against a marble landing outside the rendered window
            frame[tick] = value[0]  # => e.g. "a1" -> 'a' -- enough to visually place it on the diagram
    return "".join(frame) + ">"  # => trailing '>' marks the timeline continuing onward, standard marble notation


DEBOUNCE_QUIET = 2  # => how many silent ticks must pass before a debounced marble is allowed through
TIMELINE_LENGTH = 11  # => wide enough to render every marble in this example, including the debounce delay


if __name__ == "__main__":  # => module entry point
    merged = merge_marbles(SOURCE_A, SOURCE_B)  # => step 1: interleave A and B by tick
    print(f"merge:    {render_timeline(merged, TIMELINE_LENGTH)}")  # => Output: merge:    abba---ab-->

    mapped = map_marbles(merged, str.upper)  # => step 2: transform each value (marble stays at the same tick)
    print(f"map:      {render_timeline(mapped, TIMELINE_LENGTH)}")  # => Output: map:      ABBA---AB-->  (same shape)

    debounced = debounce_marbles(mapped, DEBOUNCE_QUIET)  # => step 3: collapse each burst to its last, quiet marble
    print(f"debounce: {render_timeline(debounced, TIMELINE_LENGTH)}")  # => Output: debounce: -----A----B>  (2 survivors)
    print(f"debounced values: {debounced}")  # => Output: [(5, 'A2'), (10, 'B3')]

    # => `merge` only reorders by time -- it never changes a value or drops one. `map` only changes
    # => VALUES -- it never moves a marble in time, which is why the rendered shape is identical
    # => before and after. `debounce` is the one operator here that changes BOTH: it deletes every
    # => marble that had a successor arrive within the quiet window (a1/b1/b2/a3 all die because
    # => something followed them too soon), and it DELAYS each survivor by the quiet period itself
    # => (A2 at tick 3 doesn't fire until tick 5) -- the cost of "wait to be sure nothing else is
    # => coming" is always some added latency. Composing operators this way -- each doing exactly
    # => one job on the (tick, value) stream -- is the same mental model marble diagrams exist to
    # => teach: read left to right, track what survives, and note where the timeline shifts.
    assert merged == [(0, "a1"), (1, "b1"), (2, "b2"), (3, "a2"), (7, "a3"), (8, "b3")]  # => strict tick order
    assert mapped == [(0, "A1"), (1, "B1"), (2, "B2"), (3, "A2"), (7, "A3"), (8, "B3")]  # => same ticks, upper values
    assert debounced == [(5, "A2"), (10, "B3")]  # => only the two marbles that had 2+ quiet ticks after them
    print("ex-87 OK")  # => Output: ex-87 OK
