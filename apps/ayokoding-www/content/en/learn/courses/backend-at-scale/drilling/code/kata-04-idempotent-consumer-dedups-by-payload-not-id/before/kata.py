# pyright: strict
"""Kata 4 (before): idempotent consumer dedups by PAYLOAD, not by message id."""

from dataclasses import dataclass, field


@dataclass
class Message:
    id: str
    body: str


@dataclass
class Consumer:
    seen_bodies: set[str] = field(default_factory=set[str])  # BUG: dedups on body, not id
    applied: list[str] = field(default_factory=list[str])

    def process(self, msg: Message) -> str:
        # THE BUG: deduping on BODY means two genuinely different messages with the
        # same body are conflated, and the same body under different ids is wrongly skipped.
        if msg.body in self.seen_bodies:  # BUG: should be msg.id
            return "skipped"
        self.seen_bodies.add(msg.body)
        self.applied.append(msg.id)
        return "applied"


c = Consumer()
# Two DIFFERENT messages that happen to share a body (e.g. "retry" payloads).
m1 = Message(id="msg-1", body="charge $10")
m2 = Message(id="msg-2", body="charge $10")  # a genuinely different charge
print(f"msg-1: {c.process(m1)}")  # applied
print(f"msg-2: {c.process(m2)}")  # BUG: skipped -- a second genuine charge was lost
