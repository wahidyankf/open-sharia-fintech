# pyright: strict
# Same strict-typing baseline as Example 57 -- no extra stub configuration
# needed beyond the installed psycopg package.
"""Example 58: Phantom Read (Prevented by PostgreSQL's Snapshot Isolation)."""

# No time import -- like Example 57, this measures ISOLATION behavior, not
# elapsed performance.
import psycopg

DSN = "host=localhost port=55432 dbname=asqp user=asqp password=asqp"
# => connection string -- readers should substitute their own PostgreSQL 18 instance


# A phantom read is a DIFFERENT anomaly from Example 57's non-repeatable read:
# instead of an EXISTING row changing value, a NEW row appears that matches
# a range condition the transaction already evaluated.
# The word "phantom" comes directly from the SQL-92 standard's terminology --
# it is the third classic isolation anomaly alongside dirty reads and
# non-repeatable reads.
def setup(conn: psycopg.Connection) -> None:  # => resets state -- fully self-contained
    """Create a small order table for the phantom-read demo."""
    with conn.cursor() as cur:
        cur.execute("SET client_min_messages TO WARNING")
        cur.execute("DROP TABLE IF EXISTS order_amount CASCADE")
        cur.execute(
            "CREATE TABLE order_amount(id INTEGER PRIMARY KEY, amount NUMERIC(10,2) NOT NULL)"
        )
        # Three starting rows, deliberately split around the amount > 100 boundary --
        # this makes the COUNT(*) below a clean, easy-to-follow number (2), not an
        # edge case at exactly 100.
        cur.execute(
            "INSERT INTO order_amount(id, amount) VALUES (1, 150.00), (2, 200.00), (3, 50.00)"
        )
        # => 2 rows already match "amount > 100" (id=1, id=2) -- id=3 does not
    conn.commit()


# This is Example 57's REPEATABLE READ demo generalized from a single-row
# UPDATE to a range-matching INSERT -- proving PostgreSQL's snapshot isolation
# blocks phantom rows the same way it blocks non-repeatable reads.
def main() -> None:  # => the script's entry point
    session_a = psycopg.connect(DSN)  # => session A: runs the SAME range query twice
    session_b = psycopg.connect(
        DSN
    )  # => session B: inserts a NEW matching row between reads
    setup(session_a)

    with session_a.cursor() as cur_a:
        # Same explicit ISOLATION LEVEL REPEATABLE READ as Example 57 -- Postgres's
        # default READ COMMITTED would let session B's new row show up immediately.
        cur_a.execute("BEGIN ISOLATION LEVEL REPEATABLE READ")
        # COUNT(*) with a range predicate, not a single-row lookup by id -- phantoms
        # are specifically about ROW SETS that satisfy a condition, not individual
        # row values.
        cur_a.execute("SELECT COUNT(*) FROM order_amount WHERE amount > 100")
        first_count = cur_a.fetchone()
        print(f"Session A first count: {first_count}")
        # => Output: Session A first count: (2,)

        with (
            session_b.cursor() as cur_b
        ):  # => session B: inserts a NEW row that matches the range
            cur_b.execute("INSERT INTO order_amount(id, amount) VALUES (4, 300.00)")
            session_b.commit()
            # => a fresh row matching "amount > 100" now exists and is COMMITTED --
            # => the SQL standard calls a newly-visible matching row a "phantom"

        # Re-running the IDENTICAL range query inside the same still-open transaction --
        # under the SQL standard's minimum REPEATABLE READ, this count would be
        # permitted to change to 3.
        cur_a.execute("SELECT COUNT(*) FROM order_amount WHERE amount > 100")
        second_count = cur_a.fetchone()
        print(f"Session A second count: {second_count}")
        # => Output: Session A second count: (2,)
        # => STILL 2 (co-14): the SQL standard's REPEATABLE READ still permits phantoms,
        # => but PostgreSQL's REPEATABLE READ is true snapshot isolation -- STRONGER than
        # => the standard requires -- so the new row stays invisible for this whole transaction
        assert first_count == second_count
        # => proves PostgreSQL's actual guarantee exceeds the SQL standard's minimum here
        session_a.commit()

    session_a.close()  # => always close what you open
    session_b.close()  # => both sessions cleaned up


# The row inserted by session B is NOT lost -- it becomes visible to session A
# the moment A starts a fresh transaction, exactly like Example 57's committed
# balance update.
if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => entry point -- runs everything above when executed as a script
