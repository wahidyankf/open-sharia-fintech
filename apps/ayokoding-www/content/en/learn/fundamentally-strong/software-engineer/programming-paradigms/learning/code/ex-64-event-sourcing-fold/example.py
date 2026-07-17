"""Example 64: Event Sourcing Fold."""

from dataclasses import dataclass  # => @dataclass generates __init__ for both Event and AccountState
from functools import reduce  # => reduce() folds the entire event log into one current state


@dataclass(frozen=True)  # => events are immutable facts: "what happened", never "what the state is now"
class Event:  # => frozen=True -- once recorded, a past event can never be edited
    kind: str  # => which transition this event represents, e.g. "deposited"
    amount: int = 0  # => the amount involved, 0 for events that don't carry one (e.g. "opened")


@dataclass(frozen=True)  # => state is DERIVED, never stored directly -- it's a fold over events
class AccountState:  # => frozen=True -- apply_event() always returns a NEW state, never mutates one
    balance: int = 0  # => the account's current balance, derived from folding every deposit/withdrawal
    is_open: bool = False  # => whether the account has been opened yet


def apply_event(state: AccountState, event: Event) -> AccountState:  # => PURE: (state, event) -> new state
    if event.kind == "opened":  # => event-driven: dispatch on the event's kind
        return AccountState(balance=0, is_open=True)  # => a brand new state, not a mutation of the old one
    if event.kind == "deposited":  # => next branch, only reached if "opened" didn't match
        return AccountState(balance=state.balance + event.amount, is_open=state.is_open)  # => new state with the deposit applied
    if event.kind == "withdrawn":  # => next branch, only reached if neither prior branch matched
        return AccountState(balance=state.balance - event.amount, is_open=state.is_open)  # => new state with the withdrawal applied
    return state  # => an unknown event kind leaves state unchanged rather than raising


log: list[Event] = [  # => the append-only event log -- the ONLY thing actually stored
    Event("opened"),  # => step 1: opens the account
    Event("deposited", 100),  # => step 2: +100
    Event("deposited", 50),  # => step 3: +50
    Event("withdrawn", 30),  # => step 4: -30
]  # => closes the append-only log -- every state is rebuilt by folding this list, never stored directly

live_state = reduce(apply_event, log, AccountState())  # => rebuild current state by folding the whole log
print(live_state)  # => 100 + 50 - 30 = 120, account open
# => Output: AccountState(balance=120, is_open=True)

replayed_state = reduce(apply_event, log, AccountState())  # => replay the SAME log again, independently
print(replayed_state == live_state)  # => replay must reproduce the exact same live state
# => Output: True
