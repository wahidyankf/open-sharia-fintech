# pyright: strict
"""Kata 7 (after): SELECT ... FOR UPDATE forces session B to wait for A's write."""

import psycopg

DSN = "host=localhost port=55432 dbname=asqp user=asqp password=asqp"


def setup(conn: psycopg.Connection) -> None:
    with conn.cursor() as cur:
        cur.execute("SET client_min_messages TO WARNING")
        cur.execute("DROP TABLE IF EXISTS inventory CASCADE")
        cur.execute(
            "CREATE TABLE inventory(id INTEGER PRIMARY KEY, stock INTEGER NOT NULL)"
        )
        cur.execute("INSERT INTO inventory(id, stock) VALUES (1, 10)")
    conn.commit()


def main() -> None:
    session_a = psycopg.connect(DSN)
    session_b = psycopg.connect(DSN)
    setup(session_a)

    with session_a.cursor() as cur_a, session_b.cursor() as cur_b:
        cur_a.execute("BEGIN")
        cur_b.execute("BEGIN")
        cur_b.execute("SET lock_timeout = '500ms'")

        # THE FIX: FOR UPDATE (co-16) takes an exclusive row lock -- held open
        # until session A commits or rolls back.
        cur_a.execute("SELECT stock FROM inventory WHERE id = 1 FOR UPDATE")
        stock_a = cur_a.fetchone()
        assert stock_a is not None
        print(f"Session A locked stock: {stock_a[0]}")

        # PROOF the lock is real: session B's own FOR UPDATE on the SAME row
        # blocks and times out instead of reading a stale value silently.
        try:
            cur_b.execute("SELECT stock FROM inventory WHERE id = 1 FOR UPDATE")
            print("Session B acquired the lock (unexpected)")
        except psycopg.errors.LockNotAvailable as exc:
            print(f"Session B blocked: {type(exc).__name__}")
        session_b.rollback()

        cur_a.execute("UPDATE inventory SET stock = %s WHERE id = 1", (stock_a[0] - 1,))
        session_a.commit()
        print(f"Session A wrote stock: {stock_a[0] - 1}")

        # session B retries AFTER A's commit -- now it reads the FRESH value.
        cur_b.execute("BEGIN")
        cur_b.execute("SELECT stock FROM inventory WHERE id = 1 FOR UPDATE")
        stock_b = cur_b.fetchone()
        assert stock_b is not None
        print(f"Session B locked stock: {stock_b[0]}")

        cur_b.execute("UPDATE inventory SET stock = %s WHERE id = 1", (stock_b[0] - 1,))
        session_b.commit()
        print(f"Session B wrote stock: {stock_b[0] - 1}")

    with session_a.cursor() as cur_check:
        cur_check.execute("SELECT stock FROM inventory WHERE id = 1")
        final = cur_check.fetchone()
        assert final is not None
        print(f"Final stock: {final[0]}")  # both decrements now land: 8

    session_a.close()
    session_b.close()


if __name__ == "__main__":
    main()
