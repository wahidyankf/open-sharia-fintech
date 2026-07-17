"""Example 82: Hierarchical Statechart -- Media Player.

co-36: a Harel statechart for a media player. `Playing` is a PARENT state with
two nested substates, `Normal` and `Shuffle` -- `toggle_shuffle` is handled at
the CHILD level and only makes sense while inside `Playing`. `stop` is handled
at the PARENT level: it is defined ONCE on `Playing` and applies no matter
which substate is currently active (shared transition, not duplicated per
substate). Volume is an ORTHOGONAL region -- `volume_up`/`volume_down` change
independently of which play-state/substate is active.
"""

from __future__ import annotations  # => defers type-hint evaluation for the dict[tuple[str, str], str] aliases below


class IllegalTransition(Exception):  # => raised when neither the child nor parent table has an entry
    pass  # => a plain marker exception -- no extra fields needed, the message carries the detail


# ============================================================
# The nested (child-level) transitions -- only meaningful INSIDE the Playing parent state
# ============================================================

SUBSTATE_TRANSITIONS: dict[tuple[str, str], str] = {  # => keys are (substate, event), checked FIRST in send()
    ("normal", "toggle_shuffle"): "shuffle",  # => normal -> shuffle, on toggle_shuffle
    ("shuffle", "toggle_shuffle"): "normal",  # => shuffle -> normal, on toggle_shuffle
}  # => closes the CHILD-level table -- only reachable while state == "playing"

# ============================================================
# The parent-level (shared) transitions -- apply from ANY substate of Playing
# ============================================================

PARENT_TRANSITIONS: dict[tuple[str, str], str] = {  # => keys are (state, event), checked SECOND in send()
    ("stopped", "play"): "playing",  # => enters Playing; substate defaults to "normal"
    ("playing", "stop"): "stopped",  # => co-36: ONE shared transition -- applies from EITHER substate
}  # => closes the PARENT-level table -- shared across every substate of "playing"


class MediaPlayer:  # => the composite state = (state, substate); volume is a fully independent region
    def __init__(self) -> None:  # => the constructor
        self.state = "stopped"  # => every player starts in this one top-level state
        self.substate: str | None = None  # => only meaningful while state == "playing"
        self.volume = 50  # => the ORTHOGONAL region -- never touched by play-state transitions

    def send(self, event: str) -> None:  # => the ONE method that ever changes state/substate
        # => 1. try the CHILD-level table first -- the more specific transition wins
        if self.state == "playing" and self.substate is not None:  # => only relevant while inside Playing
            child_key = (self.substate, event)  # => builds the (substate, event) lookup key
            if child_key in SUBSTATE_TRANSITIONS:  # => a CHILD-level match found
                self.substate = SUBSTATE_TRANSITIONS[child_key]  # => the child table supplies the next substate
                return  # => handled at the child level -- never falls through to the parent table

        # => 2. bubble up to the PARENT-level table -- the shared transition, regardless of substate
        parent_key = (self.state, event)  # => builds the (state, event) lookup key
        if parent_key in PARENT_TRANSITIONS:  # => a PARENT-level match found
            self.state = PARENT_TRANSITIONS[parent_key]  # => the parent table supplies the next top-level state
            self.substate = "normal" if self.state == "playing" else None  # => entering Playing resets to "normal"
            return  # => handled at the parent level

        # => 3. neither level has this event -- structurally illegal here
        raise IllegalTransition(f"event {event!r} is illegal in state {self.state!r}/{self.substate!r}")  # => honest failure

    def adjust_volume(self, delta: int) -> None:  # => the ORTHOGONAL region -- independent of state/substate
        self.volume = max(0, min(100, self.volume + delta))  # => clamps to [0, 100], never touches state/substate


if __name__ == "__main__":  # => demonstration entry point, executed only when this file is run directly
    player = MediaPlayer()  # => starts "stopped", substate None, per __init__
    player.send("play")  # => stopped -> playing (parent transition), substate defaults to normal
    print(player.state, player.substate)  # => confirms the parent transition fired
    # => Output: playing normal

    player.send("toggle_shuffle")  # => nested-state event, handled at the CHILD level
    print(player.substate)  # => confirms the child-level substate transition fired
    # => Output: shuffle

    player.adjust_volume(20)  # => the orthogonal region changes independently
    print(player.volume)  # => confirms volume moved, untouched by play-state/substate
    # => Output: 70

    player.send("stop")  # => the PARENT's shared transition -- applies even though substate is "shuffle"
    print(player.state, player.substate)  # => confirms the ONE shared parent transition fired from ANY substate
    # => Output: stopped None

    print(player.volume)  # => volume was never touched by the play-state transitions
    # => Output: 70
