"""Example 60: A Redux-Style Pure (state, action) -> state Reducer."""

from __future__ import (
    annotations,
)  # => enables the quoted forward references used below

from dataclasses import (
    dataclass,
    replace,
)  # => replace builds a NEW state from an OLD one


@dataclass(frozen=True)  # => the entire application state, immutable
class CartState:  # => the class body begins here
    items: tuple[
        str, ...
    ]  # => an immutable tuple of item names, never mutated in place
    total: float  # => the running total, replaced wholesale on every action


@dataclass(frozen=True)  # => an action: describes WHAT happened, carries no behavior
class AddItem:  # => the class body begins here
    name: str  # => the item being added
    price: float  # => the item's price


@dataclass(frozen=True)  # => a second action variant, carrying no data at all
class ClearCart:  # => the class body begins here
    pass  # => no fields -- this action needs no data to be meaningful


Action = AddItem | ClearCart  # => the ADT of every possible action this reducer accepts


def reducer(
    state: CartState, action: Action
) -> CartState:  # => PURE: (state, action) -> NEW state
    if isinstance(action, AddItem):  # => narrows action to AddItem inside this branch
        return replace(
            state, items=state.items + (action.name,), total=state.total + action.price
        )  # => the AddItem branch's new state
    return replace(
        state, items=(), total=0.0
    )  # => ClearCart resets everything, still a NEW CartState


initial_state = CartState(
    items=(), total=0.0
)  # => the starting state before any actions
actions: list[Action] = [  # => the sequence of actions this example replays
    AddItem("apple", 2.0),  # => action 1: adds an item
    AddItem("bread", 3.5),  # => action 2: adds a second item
    ClearCart(),  # => action 3: resets the cart entirely
    AddItem("milk", 4.0),  # => action 4: adds an item AFTER the reset
]  # => closes the actions list literal

final_state = (
    initial_state  # => the accumulator this replay loop rebinds, never mutates
)
for action in actions:  # => REPLAYS every action, one reducer call each
    final_state = reducer(
        final_state, action
    )  # => each call returns a BRAND NEW state, never mutates

replayed_state = (
    initial_state  # => a SECOND independent replay, from the SAME starting state
)
for action in actions:  # => replays the SAME action list a SECOND time
    replayed_state = reducer(
        replayed_state, action
    )  # => identical steps, identical inputs

# => this is the Redux/Elm reducer pattern: state transitions as pure function calls
print(final_state)  # => Output: CartState(items=('milk',), total=4.0)
print(
    final_state == replayed_state
)  # => Output: True -- replaying identical actions reproduces the SAME state
