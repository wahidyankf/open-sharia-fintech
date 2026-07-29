# pyright: strict
"""Example 70: SSE -- a one-way server->client event stream. (co-33)

Server-Sent Events (SSE) is a one-way server->client push over a plain HTTP
connection: the server writes `text/event-stream` frames (id + data) and the
client receives them in order. Part of the WHATWG HTML Living Standard.
"""

from collections import deque  # => deque: the one-way server->client channel
from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => co-33: one SSE event (an id + a data line)
class Event:
    id: int  # => the event id (lets the client resume with Last-Event-ID)
    data: str  # => the event payload


@dataclass  # => co-33: a one-way SSE stream (server pushes, client only receives)
class SSEStream:
    buffer: deque[Event] = field(default_factory=deque[Event])  # => events the server has pushed

    def push(self, data: str) -> Event:  # => the server pushes an event (client cannot push back)
        event_id = (self.buffer[-1].id + 1) if self.buffer else 1  # => monotonic ids
        event = Event(id=event_id, data=data)  # => build the event
        self.buffer.append(event)  # => co-33: server -> client, one direction only
        return event  # => the pushed event

    def client_recv(self) -> Event | None:  # => the client reads the next event in order
        if not self.buffer:  # => nothing pushed yet
            return None  # => idle
        return self.buffer.popleft()  # => the next event, in order


stream = SSEStream()  # => co-33: a one-way text/event-stream
stream.push("tick")  # => server pushes event 1
stream.push("tock")  # => server pushes event 2
stream.push("boom")  # => server pushes event 3

received = [stream.client_recv() for _ in range(3)]  # => client drains them in order
for ev in received:  # => print each as it arrived
    assert ev is not None  # => type-narrow
    print(f"received event id={ev.id}: {ev.data!r}")  # => Output: tick, tock, boom in order

assert [ev.data for ev in received if ev is not None] == ["tick", "tock", "boom"]  # => co-33: one-way, in order
