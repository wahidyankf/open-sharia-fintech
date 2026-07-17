"""Example 60: pytest verification for A Redux-Style Pure Reducer."""

from example import Action, AddItem, CartState, reducer


def test_replaying_actions_reproduces_the_state() -> None:
    actions: list[Action] = [AddItem("a", 1.0), AddItem("b", 2.0)]
    state_1 = CartState(items=(), total=0.0)
    for action in actions:
        state_1 = reducer(state_1, action)

    state_2 = CartState(items=(), total=0.0)
    for action in actions:
        state_2 = reducer(state_2, action)

    assert state_1 == state_2 == CartState(items=("a", "b"), total=3.0)


# => Run: pytest -- Output: 1 passed
