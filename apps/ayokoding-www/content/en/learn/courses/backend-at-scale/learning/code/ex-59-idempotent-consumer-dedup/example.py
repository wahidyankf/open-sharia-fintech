# pyright: strict
"""Example 59: Idempotent consumer -- dedup by message id. (co-29)

At-least-once delivery (co-28) means a consumer can see the SAME message
more than once. An idempotent consumer records every processed message id
and DISCARDS duplicates, so a redelivery has no effect. Source:
microservices.io -- Idempotent Consumer.
"""

from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => co-29: one message
class Message:
    id: str  # => the dedup key -- the same across redeliveries
    body: str  # => the payload


@dataclass  # => co-29: a consumer that remembers every id it has processed
class IdempotentConsumer:
    seen: set[str] = field(default_factory=set[str])  # => processed message ids
    applied: list[str] = field(default_factory=list[str])  # => bodies ACTUALLY applied (for inspection)

    def process(self, msg: Message) -> str:  # => returns "applied" or "duplicate (skipped)"
        if msg.id in self.seen:  # => co-29: this id was already processed -> discard the duplicate
            return "duplicate (skipped)"  # => no effect
        self.seen.add(msg.id)  # => record the id as processed
        self.applied.append(msg.body)  # => apply the side effect ONCE
        return "applied"  # => genuinely new -> applied


consumer = IdempotentConsumer()  # => co-29: remembers processed ids
msg = Message(id="msg-1", body="charge $10")  # => the original message

first = consumer.process(msg)  # => genuinely new -> applied
print(f"first delivery:  {first}, applied={consumer.applied}")  # => Output: applied, ['charge $10']

redelivery = consumer.process(msg)  # => co-29: SAME id redelivered -> discarded
print(f"redelivery:      {redelivery}, applied={consumer.applied}")  # => Output: skipped, still ['charge $10']

assert first == "applied" and redelivery == "duplicate (skipped)"  # => co-29: duplicate detected + skipped
assert consumer.applied == ["charge $10"]  # => the body was applied exactly ONCE despite two deliveries
