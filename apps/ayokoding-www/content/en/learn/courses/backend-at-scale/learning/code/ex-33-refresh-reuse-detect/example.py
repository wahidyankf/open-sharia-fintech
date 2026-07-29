# pyright: strict
"""Example 33: Refresh-token reuse detection. (co-18)

If a refresh token that was ALREADY rotated out is presented again, that
means an attacker stole the original and is trying to use it after the
legitimate client already rotated. Detection REVOKESS the entire token
family, invalidating every token derived from the original sign-in.
"""

from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => co-18: tracks a token family so reuse can revoke the whole chain
class RefreshStore:
    active: set[str] = field(default_factory=lambda: {"r-0"})  # => currently-valid refresh tokens
    used: set[str] = field(default_factory=set[str])  # => refresh tokens already rotated OUT
    revoked: bool = False  # => whether the family has been burned by a detected reuse
    counter: list[int] = field(default_factory=lambda: [1])  # => a mutable counter cell


def rotate(store: RefreshStore, presented: str) -> str | None:  # => co-18: rotate, OR detect reuse + revoke
    if store.revoked:  # => the family was already burned by a prior reuse detection
        return None  # => nothing issues anymore
    if presented in store.used:  # => co-18: a USED-then-rotated token reappears -> REUSE DETECTED
        store.active.clear()  # => revoke the ENTIRE family -- every active token is now invalid
        store.revoked = True  # => mark the family burned so all future calls short-circuit
        return None  # => signal: reuse detected, family revoked
    if presented not in store.active:  # => a refresh that was never valid in this family
        return None  # => rejected
    store.active.remove(presented)  # => the used token leaves the active set
    store.used.add(presented)  # => ...and lands in the used set, so a replay triggers detection
    new_token = f"r-{store.counter[0]}"  # => mint the next token in the family
    store.counter[0] += 1  # => advance
    store.active.add(new_token)  # => the new token is now the active one
    return new_token  # => the rotated refresh


store = RefreshStore()  # => co-18: one family's state

first = rotate(store, "r-0")  # => co-18: legitimate rotation -> new active token
assert first is not None  # => type-narrow
print(f"legitimate rotation: {first}")  # => Output: r-1

attacker_replay = rotate(store, "r-0")  # => co-18: the STOLEN, already-used token -> REUSE DETECTED
print(f"attacker replays stolen r-0: {attacker_replay} (family revoked)")  # => Output: None

legit_after_breach = rotate(store, first)  # => co-18: even the legitimate new token is now revoked
print(f"legitimate client uses r-1 after breach: {legit_after_breach}")  # => Output: None -- family burned

assert attacker_replay is None and legit_after_breach is None  # => co-18: reuse revoked the whole family
assert store.revoked and len(store.active) == 0  # => co-18: no active token survives a detected reuse
