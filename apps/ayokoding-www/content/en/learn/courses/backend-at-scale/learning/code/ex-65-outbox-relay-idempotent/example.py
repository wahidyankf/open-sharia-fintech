# pyright: strict
"""Example 65: Outbox relay is at-least-once; the consumer keeps effects once. (co-13, co-29)

The transactional-outbox relay (co-13) publishes at-LEAST-once -- it may
publish the SAME message twice (e.g. it crashes after publishing but before
marking it sent). The downstream idempotent consumer (co-29) keeps the
effect exactly once, so a duplicate relay delivery is harmless.
"""

from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => co-13: a relay that may redeliver, plus the outbox it drains
class Relay:
    outbox: list[str] = field(default_factory=list[str])  # => committed messages awaiting publish
    published: list[str] = field(default_factory=list[str])  # => every publish attempt (incl. duplicates)
    crash_before_marking_sent: bool = True  # => co-13: simulates a crash after publish, before marking sent

    def publish_all(self) -> list[str]:  # => co-13: at-least-once publish (may emit a message twice)
        emitted: list[str] = []  # => what was emitted this round
        for msg in list(self.outbox):  # => drain the outbox
            self.published.append(msg)  # => record the publish attempt
            emitted.append(msg)  # => emit it
        if self.crash_before_marking_sent:  # => co-13: crashed before clearing the outbox
            self.outbox = list(self.outbox)  # => outbox NOT cleared -> messages will be re-published
        else:  # => cleanly marked sent
            self.outbox.clear()  # => outbox cleared
        return emitted  # => this round's emissions


BALANCE = [0]  # => the side-effect target


@dataclass  # => co-29: an idempotent consumer guards the side effect
class WalletConsumer:
    seen: set[str] = field(default_factory=set[str])  # => processed message ids

    def apply(self, msg_id: str, amount: int) -> str:  # => returns "applied" or "duplicate"
        if msg_id in self.seen:  # => co-29: duplicate -> skip
            return "duplicate"  # => no effect
        self.seen.add(msg_id)  # => record the id
        BALANCE[0] += amount  # => apply ONCE
        return "applied"  # => applied


relay = Relay(outbox=["credit:100"])  # => co-13: one committed message in the outbox
consumer = WalletConsumer()  # => co-29: guards the balance

round1 = relay.publish_all()  # => co-13: publishes, then "crashes" before marking sent
for m in round1:  # => consumer handles round 1
    consumer.apply(m, 100)  # => applied once
print(f"round 1 published: {round1}, balance: {BALANCE[0]}")  # => Output: ['credit:100'], 100

relay.crash_before_marking_sent = False  # => co-13: next round marks sent cleanly
round2 = relay.publish_all()  # => co-13: the SAME message redelivered (at-least-once)
for m in round2:  # => consumer handles round 2
    result = consumer.apply(m, 100)  # => co-29: duplicate -> skipped
    print(f"  redelivered {m}: {result}")  # => Output: duplicate
print(f"round 2 published: {round2}, balance: {BALANCE[0]}")  # => Output: redelivered, balance still 100

assert relay.published.count("credit:100") == 2  # => co-13: the relay published twice (at-least-once)
assert BALANCE[0] == 100  # => co-29: the consumer applied the effect exactly ONCE
