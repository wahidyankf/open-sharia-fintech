# pyright: strict
"""Capstone: run_scenario.py -- wires every prior step into ONE mini-ORM and runs the same
customers/orders scenario topic 27 ran over a real framework: migrations.py creates the
schema (co-24); unit_of_work.py inserts three customers and their orders in dependency
order (co-16, co-19, co-20); session.py + identity_map.py prove one object per loaded
primary key (co-13, co-15); unit_of_work.py's dirty tracking updates only a changed column
(co-17) and deletes one order (co-18); a UNIQUE-email collision proves flush() rolls back
the ENTIRE batch, not just the failing row (co-20); lazy.py demonstrates the N+1 its own
descriptor can cause, then the eager fix that collapses it to 2 queries (co-21, co-22) --
proving the same result topic 27's real ORM produced, now with every mechanism visible and
hand-built.
"""

import contextlib
import datetime
import sqlite3

import lazy
import migrations
from domain import Customer, Order
from mapper import load_customer
from session import Session
from unit_of_work import UnitOfWork


def main() -> None:
    with contextlib.closing(sqlite3.connect(":memory:")) as conn:
        applied = migrations.migrate(conn)  # => co-24: schema created FIRST, before anything else touches it
        print(f"migrations applied: {applied}")  # => Output: migrations applied: [1, 2]

        # Step A -- co-16, co-19, co-20: three new customers, each with orders, ONE atomic flush.
        with Session(conn) as session:
            uow = UnitOfWork(session)
            ada = Customer(id=None, name="Ada", email="ada@example.com")
            bob = Customer(id=None, name="Bob", email="bob@example.com")
            carol = Customer(id=None, name="Carol", email="carol@example.com")
            for customer in (ada, bob, carol):
                uow.register_new_customer(customer)  # => co-16: tracked -- NO SQL runs yet
            today = datetime.date(2026, 7, 18)
            uow.register_new_order(Order(id=None, customer_id=-1, item="Keyboard", amount=79.5, placed_on=today), ada)
            uow.register_new_order(Order(id=None, customer_id=-1, item="Monitor", amount=199.0, placed_on=today), ada)
            uow.register_new_order(Order(id=None, customer_id=-1, item="Mouse", amount=25.0, placed_on=today), bob)
            # => co-19: every order above references its PARENT OBJECT -- customer_id=-1 is a placeholder,
            # resolved to the REAL pk only once flush() inserts the parent first.
            uow.flush()  # => co-20: 3 customers + 3 orders, ONE transaction, ONE commit
            print(f"ada.id={ada.id} bob.id={bob.id} carol.id={carol.id}")  # => Output: ada.id=1 bob.id=2 carol.id=3
            row_count = conn.execute("SELECT COUNT(*) FROM customer_order").fetchone()[0]
            print(f"orders after step A: {row_count}")  # => Output: orders after step A: 3

        # Step B -- co-13, co-15: the identity map returns the SAME object for the SAME pk, twice.
        assert ada.id is not None  # => real by now -- step A's flush() already assigned it
        with Session(conn) as session:
            row = conn.execute("SELECT id, name, email FROM customer WHERE id = ?", (ada.id,)).fetchone()
            first_load = load_customer(row)  # => co-10: mapped from the row
            session.identity_map.put("customer", ada.id, first_load)  # => co-13: registered
            cached = session.identity_map.get("customer", ada.id, Customer)  # => co-13: a cache HIT, no new query
            print(f"same instance: {cached is first_load}")  # => Output: same instance: True
            assert cached is first_load  # => co-13's core guarantee

        # Step C -- co-17: mutate a loaded customer's email, flush, UPDATE touches only that column.
        with Session(conn) as session:
            uow = UnitOfWork(session)
            row = conn.execute("SELECT id, name, email FROM customer WHERE id = ?", (bob.id,)).fetchone()
            loaded_bob = load_customer(row)
            uow.track_clean(loaded_bob)  # => co-17: snapshot taken NOW, at load time
            loaded_bob.email = "bob@newmail.com"  # => mutates the LIVE object -- name stays untouched
            dirty = uow.dirty_objects()
            print(f"dirty count: {len(dirty)}")  # => Output: dirty count: 1
            uow.flush()  # => co-17 + co-20: the UPDATE's SET clause contains ONLY the email column
            refreshed = conn.execute("SELECT name, email FROM customer WHERE id = ?", (bob.id,)).fetchone()
            print(f"bob after update: {refreshed}")  # => Output: bob after update: ('Bob', 'bob@newmail.com')
            assert refreshed == ("Bob", "bob@newmail.com")  # => name untouched -- only the changed column moved

        # Step D -- co-18: delete one of Ada's two orders.
        with Session(conn) as session:
            uow = UnitOfWork(session)
            deletable_row = conn.execute("SELECT id, customer_id, item, amount, placed_on FROM customer_order WHERE item = ?", ("Mouse",)).fetchone()
            mouse_order = Order(
                id=deletable_row[0],
                customer_id=deletable_row[1],
                item=deletable_row[2],
                amount=deletable_row[3],
                placed_on=datetime.date.fromisoformat(deletable_row[4]),
            )
            uow.register_deleted(mouse_order)  # => co-18: tracked -- NO SQL runs yet
            uow.flush()  # => co-18 + co-20: the DELETE runs, committed atomically
            remaining = conn.execute("SELECT COUNT(*) FROM customer_order").fetchone()[0]
            print(f"orders after step D: {remaining}")  # => Output: orders after step D: 2

        # Step E -- co-20: a UNIQUE-email collision rolls back the ENTIRE flush, not just the failing row.
        with Session(conn) as session:
            uow = UnitOfWork(session)
            dave = Customer(id=None, name="Dave", email="dave@example.com")  # => a genuinely new, non-colliding row
            eve = Customer(id=None, name="Eve", email="ada@example.com")  # => DELIBERATE: collides with Ada's email
            uow.register_new_customer(dave)  # => tracked alongside eve -- BOTH sit in the SAME flush() batch
            uow.register_new_customer(eve)
            try:
                uow.flush()  # => co-20: dave's INSERT succeeds first, then eve's hits the UNIQUE constraint
                raise AssertionError("expected an IntegrityError -- the UNIQUE constraint should have fired")
            except sqlite3.IntegrityError as exc:
                print(f"IntegrityError: {exc}")  # => Output: IntegrityError: UNIQUE constraint failed: customer.email
            # => co-20: the except branch above already ran conn.rollback() -- dave's successful INSERT was
            # undone TOO, together with eve's failing one, because both shared ONE transaction.
            customer_count = conn.execute("SELECT COUNT(*) FROM customer").fetchone()[0]
            print(f"customers after failed flush: {customer_count}")  # => Output: customers after failed flush: 3
            assert customer_count == 3  # => co-20: still just Ada/Bob/Carol -- dave never actually landed
            names = {row[0] for row in conn.execute("SELECT name FROM customer").fetchall()}
            assert "Dave" not in names and "Eve" not in names  # => co-20: neither row survived the rollback
            # => CAVEAT: dave.id was still mutated to a real int mid-flush, BEFORE eve's row failed -- the
            # database's rollback is atomic, but a tracked Python OBJECT's attributes are not automatically
            # rewound to match. Never trust an object's state after a flush() you just caught an exception from.
            print(f"dave.id after rollback (stale, do not trust): {dave.id}")  # => Output: dave.id after rollback (stale, do not trust): 4

        # Step F -- co-21, co-22: lazy loading's N+1, then the eager fix, over the SAME data.
        lazy.QUERY_LOG.clear()
        all_customers = lazy.load_all_customers_naive(conn)  # => query 1
        for customer in all_customers:  # => co-22: naive per-item loop
            customer.orders  # => one SEPARATE query per customer
        naive_query_count = len(lazy.QUERY_LOG)
        print(f"naive query count: {naive_query_count}")  # => Output: naive query count: 4

        lazy.QUERY_LOG.clear()
        grouped = lazy.load_all_customers_with_orders_eager(conn)  # => co-22: the fix
        eager_query_count = len(lazy.QUERY_LOG)
        print(f"eager query count: {eager_query_count}")  # => Output: eager query count: 2
        assert eager_query_count == 2  # => co-22: exactly 2, regardless of how many customers exist
        assert naive_query_count == 1 + len(all_customers)  # => co-22: 1 + N, observably worse than the fix

        total_orders = sum(len(orders) for orders in grouped.values())
        print(f"total orders across all customers: {total_orders}")  # => Output: total orders across all customers: 2
        assert total_orders == 2  # => matches step D's remaining count exactly -- both layers agree


if __name__ == "__main__":  # => guards against running the scenario on `import run_scenario`
    main()
