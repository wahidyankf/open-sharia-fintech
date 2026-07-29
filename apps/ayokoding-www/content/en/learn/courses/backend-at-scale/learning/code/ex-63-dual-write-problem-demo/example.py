# pyright: strict
"""Example 63: The dual-write problem -- a crash loses the message. (co-12)

Writing to a DB AND a broker in one step cannot be made atomic across BOTH:
if the process crashes between the DB commit and the broker publish, the DB
write survives but the message is LOST. This example demonstrates the loss.
Source: microservices.io -- the dual-write problem.
"""

from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => co-12: a process with a DB and a broker, plus a crash switch
class Service:
    db: list[str] = field(default_factory=list[str])  # => the committed DB writes
    broker: list[str] = field(default_factory=list[str])  # => the published broker messages
    crash_before_publish: bool = False  # => co-12: simulate a crash between commit and publish

    def place_order(self, order: str) -> None:  # => the dual-write: commit to DB, then publish
        self.db.append(order)  # => WRITE 1: committed to the DB
        if self.crash_before_publish:  # => co-12: CRASH right here -- the process dies
            return  # => the DB write survived, but the publish never happened
        self.broker.append(order)  # => WRITE 2: published to the broker (skipped on crash)


happy = Service()  # => co-12: no crash
happy.place_order("order-A")  # => both writes succeed
print(f"happy path: db={happy.db}, broker={happy.broker}")  # => Output: both have order-A

crashed = Service(crash_before_publish=True)  # => co-12: crash between the two writes
crashed.place_order("order-B")  # => DB committed, then the process "died" before publishing
print(f"crash path: db={crashed.db}, broker={crashed.broker}")  # => Output: db has order-B, broker is EMPTY
print("dual-write result: order-B is committed but its event was LOST")  # => Output: the lost message

assert happy.db == ["order-A"] and happy.broker == ["order-A"]  # => happy path: both consistent
assert crashed.db == ["order-B"] and crashed.broker == []  # => co-12: the message was lost in the crash
