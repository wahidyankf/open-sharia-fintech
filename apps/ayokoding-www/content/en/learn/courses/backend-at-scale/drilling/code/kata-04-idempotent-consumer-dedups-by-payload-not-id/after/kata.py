# pyright: strict
"""Kata 4 (after): idempotent consumer dedups by message ID."""

from dataclasses import dataclass, field


@dataclass
class Message:
    id: str
    body: str


@dataclass
class Consumer:
    seen_ids: set[str] = field(default_factory=set[str])  # THE FIX: dedup on message id
    applied: list[str] = field(default_factory=list[str])

    def process(self, msg: Message) -> str:
        if msg.id in self.seen_ids:  # THE FIX: same id (a redelivery) -> skip
            return "skipped"
        self.seen_ids.add(msg.id)
        self.applied.append(msg.id)
        return "applied"


c = Consumer()
m1 = Message(id="msg-1", body="charge $10")
m2 = Message(id="msg-2", body="charge $10")  # a genuinely different charge -> different id
redeliver = Message(id="msg-1", body="charge $10")  # a redelivery of msg-1 -> same id
print(f"msg-1:       {c.process(m1)}")  # applied
print(f"msg-2:       {c.process(m2)}")  # applied (different id, even though same body)
print(f"redeliver:   {c.process(redeliver)}")  # skipped (same id as msg-1)
assert c.applied == ["msg-1", "msg-2"]
