"""Example 40: Event-Driven Loop."""

from collections import deque  # => deque gives O(1) popleft(), the FIFO queue's core operation
from collections.abc import Callable  # => types every handler stored in the routing table below
from dataclasses import dataclass  # => @dataclass auto-generates Event's __init__ from its fields


@dataclass  # => auto-generates Event's __init__ from the two fields below
class Event:  # => a plain data record describing what happened
    kind: str  # => which handler should process this event, e.g. "login"
    payload: str  # => the data the handler needs, e.g. a username


processed: list[str] = []  # => records the order events were actually handled in


def on_login(event: Event) -> None:  # => handler for "login" events
    processed.append(f"login:{event.payload}")  # => the framework calls this -- it never calls the loop


def on_logout(event: Event) -> None:  # => handler for "logout" events
    processed.append(f"logout:{event.payload}")  # => same shape as on_login, different kind and record


handlers: dict[str, Callable[[Event], None]] = {"login": on_login, "logout": on_logout}  # => routing table

queue: deque[Event] = deque(  # => a FIFO queue -- events wait here until the loop drains them
    [  # => the events, already enqueued in the order they should be processed
        Event("login", "alice"),  # => first to arrive, first to be handled
        Event("login", "bob"),  # => second to arrive
        Event("logout", "alice"),  # => third to arrive
    ]  # => closes the initial list of queued events
)  # => closes the deque(...) constructor call

while queue:  # => the event loop: keep draining until the queue is empty
    event = queue.popleft()  # => take the OLDEST event first -- FIFO order
    handlers[event.kind](event)  # => route it to its handler and run that handler NOW
    # => the loop itself decides WHEN each handler runs -- the handler never calls back into the loop

print(processed)  # => events must be processed in the exact order they were enqueued
# => Output: ['login:alice', 'login:bob', 'logout:alice']
