# pyright: strict
# Same strict-typing baseline as every other psycopg example in this topic --
# no extra stub configuration needed beyond the installed psycopg package.
"""Example 57: Repeatable Read Anomaly (Prevented)."""

# No time import needed here -- this example measures TRANSACTION ISOLATION
# behavior, not elapsed wall-clock performance.
import psycopg

DSN = "host=localhost port=55432 dbname=asqp user=asqp password=asqp"
# => connection string -- readers should substitute their own PostgreSQL 18 instance


# A single-row account table is the simplest possible setup for demonstrating
# a read-read-read anomaly window between two concurrent sessions.
def setup(conn: psycopg.Connection) -> None:  # => resets state -- fully self-contained
    """Create and seed a single-row account table for the isolation demo."""
    with conn.cursor() as cur:
        cur.execute("SET client_min_messages TO WARNING")
        cur.execute("DROP TABLE IF EXISTS account CASCADE")
        # NUMERIC(10,2) again avoids floating-point rounding error for money values --
        # the assertion below (first_read == second_read) must be an EXACT match.
        cur.execute(
            "CREATE TABLE account(id INTEGER PRIMARY KEY, balance NUMERIC(10,2) NOT NULL)"
        )
        # balance starts at 500.00 -- session B will change it to 400.00 mid-transaction
        # to test whether session A's REPEATABLE READ snapshot notices.
        cur.execute("INSERT INTO account(id, balance) VALUES (1, 500.00)")
    conn.commit()


# This is the DIRECT counterpart to Example 27's default-isolation anomaly --
# same interleaving, but wrapped in REPEATABLE READ instead of READ COMMITTED
# to show the SAME code pattern producing a DIFFERENT (correct) result.
def main() -> None:  # => the script's entry point
    session_a = psycopg.connect(DSN)  # => session A: reads under REPEATABLE READ
    session_b = psycopg.connect(DSN)  # => session B: writes between A's two reads
    setup(session_a)

    with session_a.cursor() as cur_a:
        # Explicitly requesting REPEATABLE READ matters -- Postgres's default (READ
        # COMMITTED) would let session B's mid-transaction commit become visible on
        # the very next SELECT, reproducing Example 27's bug instead of fixing it.
        cur_a.execute("BEGIN ISOLATION LEVEL REPEATABLE READ")
        # => explicit REPEATABLE READ (co-13) -- unlike Example 27's default READ
        # => COMMITTED, this takes ONE consistent snapshot for the WHOLE transaction
        cur_a.execute("SELECT balance FROM account WHERE id = 1")
        first_read = cur_a.fetchone()
        print(f"Session A first read: {first_read}")
        # => Output: Session A first read: (Decimal('500.00'),)

        # Session B is a COMPLETELY separate connection and transaction -- from
        # Postgres's point of view these two sessions have no relationship beyond
        # both touching the same row.
        with (
            session_b.cursor() as cur_b
        ):  # => session B: independent, commits mid-flight
            cur_b.execute("UPDATE account SET balance = 400.00 WHERE id = 1")
            session_b.commit()
            # => session B commits a DIFFERENT value WHILE session A's transaction
            # => is still open -- the SAME interleaving that broke Example 27

        cur_a.execute("SELECT balance FROM account WHERE id = 1")
        second_read = cur_a.fetchone()
        print(f"Session A second read: {second_read}")
        # => Output: Session A second read: (Decimal('500.00'),)
        # => UNCHANGED (co-14): REPEATABLE READ's snapshot was taken at BEGIN and
        # => never moves -- session B's commit is INVISIBLE until A's own transaction ends
        assert first_read == second_read
        # => proves the anomaly from Example 27 is GONE under REPEATABLE READ
        # Committing session A's transaction here ends its snapshot -- any FUTURE
        # query on this connection will take a brand-new one.
        session_a.commit()

    # A fresh cursor block does not by itself start a new transaction in
    # psycopg's default autocommit=False mode -- but the PRIOR commit() above
    # already closed the old transaction, so this next execute() implicitly
    # opens a new one with a fresh snapshot.
    with session_a.cursor() as cur_a:
        cur_a.execute("SELECT balance FROM account WHERE id = 1")
        after_commit = cur_a.fetchone()
        print(f"Session A read after commit: {after_commit}")
        # => Output: Session A read after commit: (Decimal('400.00'),)
        # => a NEW transaction takes a NEW snapshot -- now B's committed value IS visible

    session_a.close()  # => always close what you open
    session_b.close()  # => both sessions cleaned up


# Compare this script's assertion (first_read == second_read, PROVEN true)
# against Example 27, where the equivalent assertion would FAIL -- that
# contrast is the entire teaching point of REPEATABLE READ isolation.
if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => entry point -- runs everything above when executed as a script
