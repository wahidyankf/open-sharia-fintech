# pyright: strict
"""Example 61: Dead-letter queue -- a poison message is sidelined. (co-30)

A poison message fails processing every time it is delivered. After it
exceeds `maxReceiveCount`, the broker moves it to a dead-letter queue (DLQ)
for later inspection, instead of redelivering it forever. Source: AWS SQS
dead-letter queues.
"""

from collections import deque  # => deque: FIFO queues for main + DLQ
from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => co-30: one message
class Message:
    id: str  # => the message id
    poison: bool  # => True = always fails processing


@dataclass  # => co-30: a broker with a main queue, receive counters, and a DLQ
class Broker:
    main: deque[Message] = field(default_factory=deque[Message])  # => messages awaiting processing
    receive_counts: dict[str, int] = field(default_factory=dict[str, int])  # => deliveries per id
    dlq: list[str] = field(default_factory=list[str])  # => ids sidelined to the DLQ
    max_receive_count: int = 3  # => co-30: after this many failed receives, move to the DLQ
    processed: list[str] = field(default_factory=list[str])  # => ids successfully processed

    def deliver(self, msg: Message) -> None:  # => enqueue a message
        self.main.append(msg)  # => to the back of the main queue

    def process_one(self) -> str:  # => pull, attempt, and either ack / requeue / dead-letter
        if not self.main:  # => nothing to process
            return "idle"  # => no-op
        msg = self.main.popleft()  # => pull the front message
        self.receive_counts[msg.id] = self.receive_counts.get(msg.id, 0) + 1  # => count this receive
        if msg.poison and self.receive_counts[msg.id] >= self.max_receive_count:  # => co-30: exceeded the limit
            self.dlq.append(msg.id)  # => sideline to the DLQ
            return f"dead-lettered {msg.id}"  # => removed from circulation
        if msg.poison:  # => co-30: failed but under the limit -> redeliver
            self.main.append(msg)  # => re-queue for another attempt
            return f"failed {msg.id} (receive {self.receive_counts[msg.id]})"  # => will retry
        self.processed.append(msg.id)  # => good message -> acked
        return f"processed {msg.id}"  # => success


b = Broker()  # => co-30: maxReceiveCount=3
b.deliver(Message("good-1", poison=False))  # => a healthy message
b.deliver(Message("poison-9", poison=True))  # => a poison message

log = [b.process_one() for _ in range(6)]  # => drain the queue (good succeeds, poison retries then DLQs)
for line in log:  # => print each processing step
    print(line)  # => Output: processed good-1, then poison retries, then dead-lettered
print(f"DLQ: {b.dlq}, processed: {b.processed}")  # => Output: poison-9 sidelined, good-1 done

assert "poison-9" in b.dlq and "good-1" in b.processed  # => co-30: poison dead-lettered, good processed
assert b.receive_counts["poison-9"] == b.max_receive_count  # => co-30: dead-lettered exactly at the limit
