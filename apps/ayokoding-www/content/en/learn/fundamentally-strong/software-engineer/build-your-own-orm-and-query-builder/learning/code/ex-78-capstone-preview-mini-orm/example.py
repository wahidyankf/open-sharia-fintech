"""Example 78: A Mini-ORM Preview -- Migrations, UnitOfWork, Identity Map, Eager Loading."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => the domain object AND the migration record, both frozen-vs-mutable as appropriate
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)


@dataclasses.dataclass(frozen=True)  # => co-24: a migration is immutable data
class Migration:  # => the smallest unit this mini-ORM's schema setup applies
    version: int  # => co-24: applied in ascending order
    sql: str  # => the raw DDL this migration executes when applied


def migrate(conn: sqlite3.Connection, migrations: list[Migration]) -> None:  # => co-24: the whole runner, compact
    conn.execute("CREATE TABLE IF NOT EXISTS schema_version(version INTEGER PRIMARY KEY)")  # => bookkeeping
    applied = {row[0] for row in conn.execute("SELECT version FROM schema_version").fetchall()}  # => already-run
    for migration in sorted(migrations, key=lambda m: m.version):  # => co-24: ascending order, always
        if migration.version not in applied:  # => co-24: SKIPS anything already recorded
            conn.executescript(migration.sql)  # => runs this migration's own DDL
            conn.execute("INSERT INTO schema_version VALUES (?)", (migration.version,))  # => records it
    conn.commit()  # => makes every applied migration durable together


@dataclasses.dataclass  # => a mutable, tracked-and-loaded domain object
class Customer:  # => the type this mini-ORM's unit of work tracks and its identity map caches
    id: int | None  # => None until flush() assigns it
    name: str  # => an ordinary column


class MiniOrm:  # => co-13 + co-20 + co-22: identity map, unit of work, and eager loading, composed
    def __init__(self, conn: sqlite3.Connection) -> None:  # => owns the connection every layer shares
        self._conn = conn  # => co-15: the ONE connection this whole mini-ORM ever uses
        self._identity_map: dict[int, Customer] = {}  # => co-13: keyed by pk, one object per row FOREVER
        self._new: list[Customer] = []  # => co-16: objects registered as "new", pending a flush

    def add(self, customer: Customer) -> None:  # => co-16: tracks a brand-new object
        self._new.append(customer)  # => appended, not written -- no SQL runs here

    def flush(self) -> None:  # => co-20: turns EVERY pending object into a real INSERT, atomically
        for customer in self._new:  # => one INSERT per tracked-new object
            cursor = self._conn.execute("INSERT INTO customers(name) VALUES (?)", (customer.name,))  # => real write
            assert cursor.lastrowid is not None  # => co-20: SQLite ALWAYS assigns a rowid on a real INSERT
            customer.id = cursor.lastrowid  # => the pk assigned by the database
            self._identity_map[customer.id] = customer  # => co-13: newly-flushed objects join the identity map too
        self._new.clear()  # => flushed objects are no longer "new"
        self._conn.commit()  # => makes every INSERT durable together

    def identity_of(self, pk: int) -> Customer:  # => co-13: the PUBLIC way to inspect a cached object's identity
        return self._identity_map[pk]  # => the SAME object every flush/load for this pk has ever produced

    def all_with_orders(self) -> dict[int, list[tuple[int, float]]]:  # => co-22: batch-loaded, never N+1
        customer_rows = self._conn.execute("SELECT id, name FROM customers").fetchall()  # => query 1: parents
        for pk, name in customer_rows:  # => co-13: reuses cached objects, never re-constructs a known pk
            if pk not in self._identity_map:  # => a genuine cache miss -- this pk has never been seen before
                self._identity_map[pk] = Customer(id=pk, name=name)  # => co-10: mapped ONCE, cached forever after
        ids = [pk for pk, _ in customer_rows]  # => every parent pk, gathered up front for the batch query
        placeholders = ",".join("?" for _ in ids)  # => one "?" per id -- an IN clause, not a per-item loop
        order_rows = self._conn.execute(  # => co-22: query 2 -- the ONLY child query, regardless of N
            f"SELECT customer_id, id, total FROM orders WHERE customer_id IN ({placeholders})",  # => dynamic IN
            ids,  # => bound safely -- co-02, never string-interpolated data
        ).fetchall()  # => the ENTIRE child dataset, in a single round trip
        grouped: dict[int, list[tuple[int, float]]] = {pk: [] for pk in ids}  # => pre-seeded per-customer buckets
        for customer_id, order_id, total in order_rows:  # => co-22: groups the ONE result set in memory
            grouped[customer_id].append((order_id, total))  # => appended to the correct customer's bucket
        return grouped  # => every customer's orders, fetched in exactly two queries total


with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    migrate(  # => co-24: schema setup, run FIRST, before anything else touches this database
        conn,  # => the same real local SQLite connection every layer below shares
        [  # => co-24: deliberately just TWO migrations, applied in ascending version order
            Migration(version=1, sql="CREATE TABLE customers(id INTEGER PRIMARY KEY, name TEXT);"),  # => parents
            Migration(version=2, sql="CREATE TABLE orders(id INTEGER PRIMARY KEY, customer_id INTEGER, total REAL);"),  # => children
        ],  # => the migration list, sorted internally by migrate() regardless of THIS order
    )  # => two migrations, applied in ascending version order
    orm = MiniOrm(conn)  # => co-13 + co-15 + co-16 + co-20: the composed mini-ORM, over ONE connection
    orm.add(Customer(id=None, name="Alice"))  # => tracked, not yet written
    orm.add(Customer(id=None, name="Bob"))  # => tracked, not yet written
    orm.flush()  # => co-20: BOTH customers written and committed together, atomically
    conn.executemany(  # => seed a couple of orders directly, to exercise the eager-load path below
        "INSERT INTO orders(customer_id, total) VALUES (?, ?)",  # => two placeholders per row
        [(1, 10.0), (1, 20.0), (2, 30.0)],  # => three orders, split across the two customers
    )  # => end of the executemany call
    conn.commit()  # => makes the seeded orders visible
    grouped = orm.all_with_orders()  # => co-22: a single call, TWO queries total, no N+1 anywhere
    assert len(grouped[1]) == 2 and len(grouped[2]) == 1  # => co-22: correctly grouped, per customer
    reloaded = orm.identity_of(1)  # => co-13: reads the SAME cached object all_with_orders() populated
    print(reloaded.name, len(grouped[1]))  # => Output: Alice 2
