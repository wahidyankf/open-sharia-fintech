# pyright: strict
"""Example 77: Connection pool -- reuse, do not reopen. (co-40)

A connection pool keeps DB connections warm and HANDS THEM OUT on check-out,
returning them on check-in so the NEXT request REUSES an existing connection
rather than paying the cost of opening a new one. The open counter proves the
second request did not trigger a new open.
"""

from collections import deque  # => deque: the pool of idle, warm connections
from dataclasses import dataclass, field  # => field: mutable-default-safe factories


@dataclass  # => co-40: one reusable DB connection (stands in for a real TCP/db connection)
class Connection:
    id: int  # => a label for which connection this is


@dataclass  # => co-40: a pool that opens connections lazily and reuses them
class ConnectionPool:
    max_size: int  # => the most connections the pool will ever hold
    idle: deque[Connection] = field(default_factory=deque[Connection])  # => warm, checked-in connections
    opens: int = 0  # => how many times a connection was actually OPENED (the cost we want to minimize)
    next_id = [1]  # => a mutable counter for new connection ids

    def checkout(self) -> Connection:  # => hand out a connection, opening one only if none is idle
        if self.idle:  # => a warm connection is available -> reuse it (no new open)
            return self.idle.popleft()  # => reused
        conn = Connection(id=self.next_id[0])  # => must open a new connection
        self.next_id[0] += 1  # => advance the id counter
        self.opens += 1  # => co-40: count the open (the cost a pool avoids on reuse)
        return conn  # => a freshly opened connection

    def checkin(self, conn: Connection) -> None:  # => return a connection to the pool for reuse
        self.idle.append(conn)  # => now warm and reusable


pool = ConnectionPool(max_size=5)  # => co-40: a small pool

# First request: no idle connection -> OPEN one (opens=1).
c1 = pool.checkout()  # => opens connection 1
print(f"first checkout: opens={pool.opens}, conn id={c1.id}")  # => Output: opens=1, id=1

pool.checkin(c1)  # => return it to the pool (now idle/warm)

# Second request: an idle connection exists -> REUSE it (opens stays 1, no new open).
c2 = pool.checkout()  # => co-40: reuses the warm connection -> no new open
print(f"second checkout: opens={pool.opens}, conn id={c2.id} (reused)")  # => Output: opens=1, id=1

assert pool.opens == 1  # => co-40: the second request REUSED a connection, not reopened
assert c2.id == c1.id  # => co-40: the same connection object was handed out again
