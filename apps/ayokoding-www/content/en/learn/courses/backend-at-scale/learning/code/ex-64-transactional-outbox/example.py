# pyright: strict
"""Example 64: Transactional outbox -- sent iff the transaction commits. (co-13)

The fix for the dual-write problem (co-12): write the outbound message into
the DB AS PART OF THE SAME TRANSACTION, then a separate relay publishes it.
Because the message and the business write commit together, the message is
"sent if and only if the transaction commits." Source: microservices.io --
Transactional Outbox (Chris Richardson).
"""

from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => co-13: a service whose DB holds an outbox table in the same transaction
class Service:
    db: list[str] = field(default_factory=list[str])  # => committed business rows
    outbox: list[str] = field(default_factory=list[str])  # => co-13: messages staged INSIDE the same transaction
    committed: bool = False  # => whether the transaction reached commit

    def place_order(self, order: str, fail: bool = False) -> None:  # => one transaction writes business + outbox
        staged_db = order  # => the business write (staged, not yet committed)
        staged_outbox = f"event:{order}"  # => co-13: the message staged IN THE SAME transaction
        if fail:  # => a mid-transaction failure -> rollback BOTH
            self.committed = False  # => neither the business write nor the message survives
            return  # => rolled back
        self.db.append(staged_db)  # => commit the business write
        self.outbox.append(staged_outbox)  # => co-13: commit the message TOGETHER with it
        self.committed = True  # => both committed atomically


def relay_publish(service: Service) -> list[str]:  # => co-13: a SEPARATE relay publishes committed outbox rows
    if not service.committed:  # => the transaction rolled back -> nothing to publish
        return []  # => no message (sent iff committed)
    published = list(service.outbox)  # => publish every committed outbox row
    service.outbox.clear()  # => the relay marks them sent
    return published  # => the published messages


committed = Service()  # => co-13: a transaction that commits
committed.place_order("order-A")  # => business + outbox commit together
published = relay_publish(committed)  # => the relay publishes the committed message
print(f"commit path: db={committed.db}, published={published}")  # => Output: db has order-A, event published

rolled_back = Service()  # => co-13: a transaction that fails
rolled_back.place_order("order-B", fail=True)  # => rollback -- neither business write nor message survives
lost = relay_publish(rolled_back)  # => co-13: nothing to publish (the transaction rolled back)
print(f"rollback path: db={rolled_back.db}, published={lost}")  # => Output: db empty, nothing published

assert committed.db == ["order-A"] and published == ["event:order-A"]  # => commit -> message sent
assert rolled_back.db == [] and lost == []  # => co-13: rollback -> message NOT sent (atomic with the business write)
