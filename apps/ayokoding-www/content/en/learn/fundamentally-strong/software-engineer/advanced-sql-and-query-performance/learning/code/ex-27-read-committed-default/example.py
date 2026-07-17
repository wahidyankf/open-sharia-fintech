# pyright: strict
# psycopg (v3) ships native type stubs -- pyright resolves conn.cursor(),
# cur.execute(), and friends to concrete types instead of Any.
"""Example 27: Read Committed Default."""

import psycopg

DSN = "host=localhost port=55432 dbname=asqp user=asqp password=asqp"
# => connection string -- readers should substitute their own PostgreSQL 18 instance
# Two independent connections again simulate two real client sessions -- the
# whole point of THIS example is what session A sees mid-transaction while
# session B commits a change underneath it.


# setup() is identical in shape to Example 26's -- reused deliberately so the
# only new concept in this file is the isolation-level anomaly itself.
def setup(conn: psycopg.Connection) -> None:  # => resets state -- fully self-contained
    """Create and seed a single-row account table for the isolation demo."""
    # Same cursor-context-manager pattern as Example 26 -- closes the cursor on exit,
    # leaves commit/rollback to the caller.
    with conn.cursor() as cur:  # => a cursor scoped to this one setup call
        cur.execute("SET client_min_messages TO WARNING")
        cur.execute("DROP TABLE IF EXISTS account CASCADE")
        cur.execute(  # => account table exists, one starting row
            "CREATE TABLE account(id INTEGER PRIMARY KEY, balance NUMERIC(10,2) NOT NULL)"
        )
        cur.execute("INSERT INTO account(id, balance) VALUES (1, 500.00)")
    # Committing here is what makes the seeded row visible to session_b's own,
    # separate transaction when it opens below.
    conn.commit()  # => makes the seed data visible to BOTH sessions opened below


# main() reads the same row TWICE inside one open transaction, with session_b's
# commit happening in between -- Read Committed's defining behavior is visible
# only because of that timing.
def main() -> None:  # => the script's entry point
    # Each connect() call is, again, its own backend process/session on the server --
    # necessary for session_b's write to be a genuinely EXTERNAL commit from
    # session_a's point of view.
    session_a = psycopg.connect(DSN)  # => session A: reads the SAME row twice
    session_b = psycopg.connect(DSN)  # => session B: writes between A's two reads
    setup(session_a)  # => seed once, using session A's connection

    # PostgreSQL's default isolation level is READ COMMITTED (co-13) -- no
    # explicit SET TRANSACTION ISOLATION LEVEL below, so this IS the default (co-12).
    # Explicit BEGIN below opens the transaction session_a will keep open across
    # BOTH reads -- without it, each cur_a.execute() would run in its OWN
    # single-statement implicit transaction and the anomaly could not be observed.
    with session_a.cursor() as cur_a:
        cur_a.execute("BEGIN")
        cur_a.execute("SELECT balance FROM account WHERE id = 1")
        # first_read captures the balance BEFORE session_b's concurrent update --
        # this is the baseline the second read will be compared against.
        first_read = cur_a.fetchone()
        print(f"Session A first read: {first_read}")
        # => Output: Session A first read: (Decimal('500.00'),)

        # session_b opens, writes, and commits ENTIRELY within this nested block --
        # by the time control returns to session_a, the write is already durable.
        with session_b.cursor() as cur_b:  # => session B: independent transaction
            # session_b's UPDATE runs in its OWN implicit transaction (no BEGIN was issued
            # on cur_b) -- psycopg auto-opens one per statement when none is active.
            cur_b.execute("UPDATE account SET balance = 400.00 WHERE id = 1")
            session_b.commit()
            # => session B commits a DIFFERENT value WHILE session A's transaction
            # => is still open -- this is the concurrent write the anomaly depends on

        # Re-issuing the IDENTICAL SELECT is deliberate -- any difference in the result
        # can only be explained by what changed in the DATABASE, not by a different query.
        cur_a.execute("SELECT balance FROM account WHERE id = 1")
        # => same statement, same still-open transaction, but a NEW value comes back
        second_read = cur_a.fetchone()
        print(f"Session A second read: {second_read}")
        # => Output: Session A second read: (Decimal('400.00'),)
        # => the value CHANGED mid-transaction (co-14) -- a non-repeatable read
        # This assertion is the example's proof, not just a comment -- if Postgres ever
        # behaved like REPEATABLE READ here instead, this line would raise AssertionError.
        assert first_read != second_read
        # => proves the anomaly: Read Committed re-reads the LATEST committed
        # => snapshot on every statement, not one snapshot for the whole transaction
        # Committing session_a now is what ends its long-lived transaction -- both reads
        # already happened, so this commit's only remaining job is to release resources.
        session_a.commit()

    # Contrast this whole scenario with REPEATABLE READ or SERIALIZABLE isolation --
    # either would have frozen session_a's snapshot at BEGIN time, so second_read
    # would still show 500.00 despite session_b's committed change.
    session_a.close()  # => always close what you open
    session_b.close()  # => both sessions cleaned up


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => entry point -- runs everything above when executed as a script
