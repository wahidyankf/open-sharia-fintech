# pyright: strict
"""Kata 7 (before): no row lock -- two sessions race a read-modify-write and lose an update."""

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
    session_a = psycopg.connect(DSN)  # => session A: one checkout decrementing stock
    session_b = psycopg.connect(DSN)  # => session B: a SECOND checkout, same item
    setup(session_a)

    with session_a.cursor() as cur_a, session_b.cursor() as cur_b:
        cur_a.execute("BEGIN")
        cur_b.execute("BEGIN")

        # BUG: plain SELECT, no FOR UPDATE -- takes no lock, so nothing stops
        # session B from reading the SAME stale value session A just read.
        cur_a.execute("SELECT stock FROM inventory WHERE id = 1")
        stock_a = cur_a.fetchone()
        assert stock_a is not None
        print(
            f"Session A read stock: {stock_a[0]}"
        )  # both sessions read stock BEFORE either writes

        cur_b.execute("SELECT stock FROM inventory WHERE id = 1")
        stock_b = cur_b.fetchone()
        assert stock_b is not None
        print(f"Session B read stock: {stock_b[0]}")

        cur_a.execute("UPDATE inventory SET stock = %s WHERE id = 1", (stock_a[0] - 1,))
        session_a.commit()
        print(f"Session A wrote stock: {stock_a[0] - 1}")

        cur_b.execute("UPDATE inventory SET stock = %s WHERE id = 1", (stock_b[0] - 1,))
        session_b.commit()
        # => session B's write OVERWRITES session A's, using the SAME stale stock_b
        # => it read before A ever wrote -- one decrement is silently lost
        print(f"Session B wrote stock: {stock_b[0] - 1}")

    with session_a.cursor() as cur_check:
        cur_check.execute("SELECT stock FROM inventory WHERE id = 1")
        final = cur_check.fetchone()
        assert final is not None
        print(f"Final stock: {final[0]}")  # expected 8 (two decrements); got 9

    session_a.close()
    session_b.close()


if __name__ == "__main__":
    main()
