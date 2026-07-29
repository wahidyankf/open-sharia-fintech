# pyright: strict
"""Example 58: At-least-once delivery -- a failed ack triggers redelivery. (co-28)

At-least-once means the broker REDELIVERS a message if the consumer does not
ack. Here the worker CRASHES before acking (simulated), so the broker puts
the message BACK on the queue for redelivery. The consumer can therefore see
the same message more than once.
"""

from collections import deque  # => deque: a simple FIFO queue
from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => co-28: one message on the queue
class Message:
    id: int  # => the message id
    body: str  # => the payload


@dataclass  # => co-28: a broker that redelivers unacked messages
class Queue:
    ready: deque[Message] = field(default_factory=deque[Message])  # => messages waiting to be delivered
    in_flight: list[Message] = field(default_factory=list[Message])  # => delivered but not yet acked
    acked: list[int] = field(default_factory=list[int])  # => ids the consumer acknowledged
    redeliveries: list[int] = field(default_factory=list[int])  # => ids that were redelivered

    def enqueue(self, msg: Message) -> None:  # => add a message to the ready queue
        self.ready.append(msg)  # => to the back

    def deliver(self) -> Message | None:  # => hand one message to the consumer (in-flight)
        if not self.ready:  # => nothing ready
            return None  # => idle
        msg = self.ready.popleft()  # => take the front message
        self.in_flight.append(msg)  # => mark it in-flight (not yet acked)
        return msg  # => the delivered message

    def ack(self, msg_id: int) -> None:  # => the consumer confirms processing
        self.in_flight = [m for m in self.in_flight if m.id != msg_id]  # => remove from in-flight
        self.acked.append(msg_id)  # => recorded as done

    def redeliver_unacked(self) -> list[int]:  # => co-28: re-queue every in-flight message NOT yet acked
        redelivered: list[int] = []  # => ids that will be sent again
        still_in_flight: list[Message] = []  # => messages that survive (already acked, kept aside)
        for msg in self.in_flight:  # => inspect every in-flight message
            if msg.id in self.acked:  # => was acked -> drop it (do not redeliver)
                continue  # => already done
            self.ready.append(msg)  # => co-28: NOT acked -> put it BACK on the ready queue
            redelivered.append(msg.id)  # => record the redelivery
        self.in_flight = still_in_flight  # => clear in-flight (acked ones are dropped)
        return redelivered  # => the ids the consumer will see AGAIN


q = Queue()  # => co-28: one broker
q.enqueue(Message(1, "send email"))  # => add message 1 to the ready queue
delivered = q.deliver()  # => hand message 1 to the consumer (in-flight, NOT acked)
assert delivered is not None  # => type-narrow
print(f"delivered message: id={delivered.id}, acked: {q.acked}")  # => Output: id=1, acked=[]

# The consumer CRASHES before acking message 1 -> the broker redelivers it.
redelivered = q.redeliver_unacked()  # => co-28: message 1 was never acked -> put back on the ready queue
print(f"redelivered (crash before ack): {redelivered}")  # => Output: [1]

# Now the consumer acks on the second delivery -> no further redelivery.
again = q.deliver()  # => redelivered message 1 handed over again
assert again is not None  # => type-narrow
q.ack(1)  # => the consumer succeeds the second time
final = q.redeliver_unacked()  # => nothing unacked remains
print(f"redelivered after ack: {final}")  # => Output: []

assert redelivered == [1]  # => co-28: the unacked message was redelivered
assert final == []  # => co-28: once acked, no further redelivery
