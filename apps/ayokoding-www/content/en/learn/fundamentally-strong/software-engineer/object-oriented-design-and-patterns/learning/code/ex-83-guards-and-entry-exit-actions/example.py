"""Example 83: Guards and Entry/Exit Actions -- Order FSM.

co-37: extends the transition-table order FSM (ex-81) with a GUARD -- `ship`
is only legal when the independent `paid` flag is true, checked ON TOP OF the
table lookup, since the table alone (confirmed -> shipped) says nothing about
payment -- plus ENTRY and EXIT actions that fire exactly once per state
crossing: `log_entry` runs once on entering a state, `release_lock` runs once
on leaving one.
"""

from __future__ import annotations  # => defers type-hint evaluation for the dataclass field annotations below

from dataclasses import dataclass, field  # => field() gives each instance its own list, not a shared mutable default


# ============================================================
# Exceptions -- two DISTINCT failure kinds: structurally illegal vs. guard-blocked
# ============================================================


class IllegalTransition(Exception):  # => the TABLE has no entry for (state, event)
    pass  # => a plain marker exception -- no extra fields needed, the message carries the detail


class GuardBlocked(Exception):  # => the table allows it, but the GUARD condition is not met
    pass  # => a SEPARATE exception type from IllegalTransition -- a different failure kind, distinctly named


# => distinguishing the two exception types lets a caller react differently: retry after payment vs. a hard bug
# => co-37: the table alone cannot know about payment -- that is what the guard in send() checks separately
ORDER_TRANSITIONS: dict[tuple[str, str], str] = {  # => keys are (state, event), values are the next state
    ("created", "confirm"): "confirmed",  # => created -> confirmed, no guard needed here
    ("confirmed", "ship"): "shipped",  # => the table says nothing about payment -- that is the guard's job
    ("shipped", "deliver"): "delivered",  # => shipped -> delivered, no guard needed here
}  # => closes the table -- structurally legal moves ONLY; payment is checked separately, in send()


@dataclass  # => generates __init__ from the field declarations below
class GuardedOrderFsm:  # => co-37: adds a guard clause plus entry/exit actions around the table lookup
    # => lock_held is separate from state/paid -- it demonstrates that exit actions can affect ANY field, not just logs
    state: str = "created"  # => every order starts in this one state
    paid: bool = False  # => an INDEPENDENT flag, set by mark_paid(), not by any state transition
    entry_log: list[str] = field(default_factory=list)  # => records every ENTRY action firing
    exit_log: list[str] = field(default_factory=list)  # => records every EXIT action firing
    lock_held: bool = True  # => simulates a resource acquired on entry, released on exit

    # => mark_paid() is the ONLY way the guard's condition ever changes -- send() only reads it
    def mark_paid(self) -> None:  # => flips the guard's condition, independent of the state machine
        self.paid = True  # => the ONE side effect -- send() below reads this flag, never sets it itself

    # => send() runs the guard/entry/exit pipeline described in the module docstring, in order
    def send(self, event: str) -> str:  # => the ONE method that ever changes state
        key = (self.state, event)  # => builds the (state, event) lookup key for the table
        if key not in ORDER_TRANSITIONS:  # => step 1: the TABLE rejects structurally illegal events
            raise IllegalTransition(f"event {event!r} is illegal in state {self.state!r}")  # => an honest, specific failure

        if event == "ship" and not self.paid:  # => co-37: the GUARD -- checked IN ADDITION to the table entry
            raise GuardBlocked("cannot ship: order is not paid")  # => the table alone said this move was legal

        old_state = self.state  # => remembers the state being LEFT, for the exit action below
        new_state = ORDER_TRANSITIONS[key]  # => the table supplies the state being ENTERED

        self._exit_action(old_state)  # => co-37: EXIT action -- fires exactly once, leaving old_state
        self.state = new_state  # => the ONE line that actually crosses state boundaries
        self._entry_action(new_state)  # => co-37: ENTRY action -- fires exactly once, entering new_state
        return self.state  # => hands back the new state to the caller

    # => entry/exit actions below are PRIVATE -- callers only ever interact through send()
    def _entry_action(self, state: str) -> None:  # => log-on-enter
        self.entry_log.append(state)  # => records exactly once per state crossing, never more

    def _exit_action(self, state: str) -> None:  # => release-lock-on-exit
        self.exit_log.append(state)  # => records exactly once per state crossing, never more
        self.lock_held = False  # => simulates releasing a resource held during the previous state
        # => in a real system, this is where a database row lock or file handle would actually be released


if __name__ == "__main__":  # => demonstration entry point, executed only when this file is run directly
    # => the SAME order instance flows through every step below -- one FSM, five successive send()/log-check calls
    fsm = GuardedOrderFsm()  # => starts "created", unpaid, per the dataclass defaults
    fsm.send("confirm")  # => created -> confirmed: exit created, entry confirmed
    print(fsm.entry_log, fsm.exit_log)  # => confirms BOTH the entry and exit actions fired exactly once
    # => Output: ['confirmed'] ['created']

    try:  # => attempts a move the table allows but the guard should block
        fsm.send("ship")  # => the TABLE allows confirmed -> shipped, but the GUARD blocks it: not yet paid
    except GuardBlocked as error:  # => the guard, not the table, produced this failure
        print(error)  # => shows the honest, specific failure message
    # => Output: cannot ship: order is not paid

    fsm.mark_paid()  # => flips the independent guard condition
    fsm.send("ship")  # => now the guard passes: exit confirmed, entry shipped
    print(fsm.state, fsm.entry_log, fsm.exit_log)  # => confirms the guard's effect and both action logs updated
    # => Output: shipped ['confirmed', 'shipped'] ['created', 'confirmed']
