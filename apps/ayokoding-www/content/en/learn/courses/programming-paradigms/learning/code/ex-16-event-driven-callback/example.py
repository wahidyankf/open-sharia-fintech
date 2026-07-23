"""Example 16: Event-Driven Callback."""

from collections.abc import Callable  # => Callable is the type hint for a plain function used as a callback
from dataclasses import dataclass, field  # => @dataclass auto-generates __init__ for Dispatcher below
# => field(default_factory=dict) gives every Dispatcher instance its own fresh dict, not a shared one


@dataclass
class Dispatcher:  # => a minimal event dispatcher: register handlers, then fire events later
    handlers: dict[str, list[Callable[[dict[str, str]], None]]] = field(default_factory=dict[str, list[Callable[[dict[str, str]], None]]])
    # => maps an event name to a list of callbacks that "answer the phone" when it fires

    def on(self, event: str, handler: Callable[[dict[str, str]], None]) -> None:  # => REGISTER a handler
        self.handlers.setdefault(event, []).append(handler)  # => attach one more listener for this event

    def fire(self, event: str, payload: dict[str, str]) -> None:  # => TRIGGER the event later
        for handler in self.handlers.get(event, []):  # => call every registered handler, in order
            handler(payload)  # => the handler runs with the payload it was given, not before this call


received: list[dict[str, str]] = []  # => where the handler below will record what it was called with


def on_user_created(payload: dict[str, str]) -> None:  # => a plain function used as a callback
    received.append(payload)  # => records the payload -- proves the handler actually ran


dispatcher = Dispatcher()  # => construct with an empty handler map
dispatcher.on("user_created", on_user_created)  # => register BEFORE anything fires -- no event yet
print(received)  # => registering alone runs nothing
# => Output: []

dispatcher.fire("user_created", {"name": "Alice"})  # => NOW the registered handler actually runs
print(received)  # => the handler ran exactly once, with the exact payload passed to fire()
# => Output: [{'name': 'Alice'}]
