"""Example 53: Enum State Tags."""

from enum import Enum  # => plain enum.Enum, not StrEnum -- keeps this example runnable on Python 3.10+


class LightState(Enum):  # => models states as a closed, named set of tags -- not raw strings
    RED = "red"  # => each member pairs a name with a value
    YELLOW = "yellow"  # => same shape as RED, a distinct named tag
    GREEN = "green"  # => same shape as RED, a distinct named tag


TRANSITIONS: dict[LightState, LightState] = {  # => the full transition table, declared as data
    LightState.RED: LightState.GREEN,  # => red -> green
    LightState.GREEN: LightState.YELLOW,  # => green -> yellow
    LightState.YELLOW: LightState.RED,  # => yellow -> red, completing the cycle
}  # => closes the transition table -- every LightState member has exactly one outgoing edge


def next_state(current: LightState) -> LightState:  # => dispatch a transition by looking up the tag
    return TRANSITIONS[current]  # => a KeyError here would mean an unmodeled state -- fails loudly, not silently


state = LightState.RED  # => start at RED
history = [state]  # => record every state visited
# => the tag never leaks into raw string comparisons anywhere in this file
for _ in range(4):  # => cycle through a full loop and then some, to prove it repeats correctly
    state = next_state(state)  # => rebind to the next tag via the transition table lookup
    history.append(state)  # => record this step before moving to the next iteration

print([s.value for s in history])  # => red -> green -> yellow -> red -> green
# => Output: ['red', 'green', 'yellow', 'red', 'green']
