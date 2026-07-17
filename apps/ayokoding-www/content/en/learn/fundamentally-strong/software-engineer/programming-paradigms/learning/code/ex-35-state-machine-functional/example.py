"""Example 35: State Machine -- Functional."""

from functools import reduce  # => reduce() is Python's built-in fold: combine a sequence into one value


def transition(state: str, event: str) -> str:  # => a PURE function: (state, event) -> new state
    if state == "locked" and event == "coin":  # => same rules as examples 33-34, expressed as pure data-in data-out
        return "unlocked"  # => no assignment to any outer variable -- just a returned value
    if state == "unlocked" and event == "push":  # => the other real transition
        return "locked"  # => same shape: a returned value, nothing mutated
    return state  # => every other combination is a no-op -- return the SAME state, no mutation anywhere


events: list[str] = ["coin", "push", "push", "coin", "coin", "push"]  # => same sequence as examples 33-34

# => a FOLD builds the whole history in one expression -- no loop body visibly mutates anything
history = reduce(  # => reduce(fn, sequence, initial) threads an accumulator through every event
    lambda states, event: states + [transition(states[-1], event)],  # => append the next state, functionally
    events,  # => the sequence being folded over, one event per step
    ["locked"],  # => the fold's starting accumulator: history begins with just the initial state
)  # => the final accumulator value IS the complete, fully-built history

print(history)  # => must be identical to examples 33-34's trace
# => Output: ['locked', 'unlocked', 'locked', 'locked', 'unlocked', 'unlocked', 'locked']
