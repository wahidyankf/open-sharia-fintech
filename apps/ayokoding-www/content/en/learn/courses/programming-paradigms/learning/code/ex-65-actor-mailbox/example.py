"""Example 65: Actor Mailbox."""

from collections import deque  # => deque gives O(1) popleft(), the mailbox's core FIFO operation
from dataclasses import dataclass, field  # => @dataclass generates __init__; field() gives fresh containers


@dataclass  # => message-passing object: state is private, only reachable via messages in its mailbox
class CounterActor:  # => auto-generates CounterActor's __init__ from the three fields below
    _mailbox: deque[str] = field(default_factory=deque[str])  # => the ONLY way to talk to this actor
    _count: int = 0  # => private state -- never touched directly from outside this class
    handled_order: list[str] = field(default_factory=list[str])  # => records the ORDER messages were processed

    def send(self, message: str) -> None:  # => enqueue a message -- does NOT process it yet
        self._mailbox.append(message)  # => arrival order is preserved by a FIFO queue

    def process_one(self) -> None:  # => process exactly ONE message from the mailbox, in arrival order
        if not self._mailbox:  # => nothing to do if the mailbox is empty
            return  # => stops here -- nothing left to process
        message = self._mailbox.popleft()  # => take the OLDEST message -- FIFO, one at a time
        self.handled_order.append(message)  # => record that this message was handled now
        if message == "increment":  # => the actor's own message-handling logic
            self._count += 1  # => mutation happens ONLY here, inside the actor, never from outside
        elif message == "decrement":  # => next branch, only reached if "increment" didn't match
            self._count -= 1  # => same private mutation, opposite direction

    def process_all(self) -> None:  # => drain the mailbox completely, one message at a time
        while self._mailbox:  # => keep going until the mailbox is empty
            self.process_one()  # => delegate to the single-message handler -- no batch shortcuts

    def read_count(self) -> int:  # => the ONLY sanctioned way to observe this actor's private state
        return self._count  # => a plain read -- never mutates, mirrors _count's private encapsulation


actor = CounterActor()  # => construct one actor with an empty mailbox
actor.send("increment")  # => enqueue, not process
actor.send("increment")  # => enqueue
actor.send("decrement")  # => enqueue
print(actor.read_count())  # => nothing processed yet -- sending alone never mutates state
# => Output: 0

actor.process_all()  # => drain the mailbox, one message at a time, in arrival order
print(actor.read_count())  # => +1 +1 -1 = 1
# => Output: 1
print(actor.handled_order)  # => confirms messages were handled in the exact order they were sent
# => Output: ['increment', 'increment', 'decrement']
