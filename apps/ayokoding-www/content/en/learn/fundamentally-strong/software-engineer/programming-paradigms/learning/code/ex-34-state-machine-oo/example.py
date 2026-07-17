"""Example 34: State Machine -- OO (State Pattern)."""

from abc import ABC, abstractmethod  # => ABC/abstractmethod force every concrete state to implement both


class TurnstileState(ABC):  # => the State pattern: each state is its OWN object, not a string tag
    @abstractmethod  # => marks on_coin() as required -- TurnstileState itself can never be instantiated
    def on_coin(self) -> "TurnstileState":  # => every state must say what a coin does to it
        ...  # => no body here -- only concrete subclasses below provide the real behavior

    @abstractmethod  # => marks on_push() as required, same contract as on_coin() above
    def on_push(self) -> "TurnstileState":  # => every state must say what a push does to it
        ...  # => no body here -- only concrete subclasses below provide the real behavior

    name: str  # => a human-readable label, set by each concrete subclass


class Locked(TurnstileState):  # => concrete state object #1
    name = "locked"  # => satisfies the abstract `name` field declared on TurnstileState

    def on_coin(self) -> TurnstileState:  # => Locked's OWN answer to "what does a coin do?"
        return Unlocked()  # => transition: return a DIFFERENT state object

    def on_push(self) -> TurnstileState:  # => Locked's OWN answer to "what does a push do?"
        return self  # => stay locked -- return the same state object, unchanged


class Unlocked(TurnstileState):  # => concrete state object #2
    name = "unlocked"  # => satisfies the same abstract `name` field, with this state's own value

    def on_coin(self) -> TurnstileState:  # => Unlocked's OWN answer to a coin
        return self  # => an extra coin changes nothing

    def on_push(self) -> TurnstileState:  # => Unlocked's OWN answer to a push
        return Locked()  # => transition back


events: list[str] = ["coin", "push", "push", "coin", "coin", "push"]  # => same sequence as example 33
current: TurnstileState = Locked()  # => start locked, as an OBJECT, not a string
history: list[str] = [current.name]  # => record the starting state's name

for event in events:  # => replay the same events
    current = current.on_coin() if event == "coin" else current.on_push()  # => dispatch via the object itself
    history.append(current.name)  # => record the new state's name

print(history)  # => must be identical to example 33's trace
# => no `if state == "locked"` anywhere -- transitions live inside each state object's own methods
# => Output: ['locked', 'unlocked', 'locked', 'locked', 'unlocked', 'unlocked', 'locked']
