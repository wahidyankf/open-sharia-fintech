# pyright: strict
# strict mode also requires every third-party call's return type to be known --
# psycopg ships its own type stubs, so calls like conn.cursor() resolve to a
# concrete Cursor type instead of falling back to Any.
"""Example 26: FOR UPDATE Row Lock."""

# psycopg (v3) is used here instead of the older psycopg2 -- v3 ships native
# type stubs and a context-manager-first API, both of which pyright --strict needs.
import psycopg

DSN = "host=localhost port=55432 dbname=asqp user=asqp password=asqp"
# => connection string -- readers should substitute their own PostgreSQL 18 instance
# Two separate DSN-based connections below (session_a, session_b) are what let
# this script simulate two independent PostgreSQL client sessions locking the
# same row -- a single connection could never demonstrate blocking against itself.


# setup() runs on session_a's connection only -- session_b simply reuses the
# already-seeded table once it connects, exactly like a second real client would.
def setup(conn: psycopg.Connection) -> None:  # => resets state -- fully self-contained
    """Create and seed a single-row account table for the lock demo."""
    # The cursor context manager closes the cursor automatically on exit -- it does
    # NOT commit or roll back the underlying transaction; that is conn.commit()'s job.
    with conn.cursor() as cur:  # => a cursor scoped to this one setup call
        # Suppressing NOTICE keeps this demo's printed output limited to the print()
        # statements below, not routine DROP/CREATE chatter from the server.
        cur.execute("SET client_min_messages TO WARNING")
        cur.execute("DROP TABLE IF EXISTS account CASCADE")
        # NUMERIC(10, 2) mirrors the same money-safe precision convention used
        # throughout this topic's SQL examples -- exact decimal arithmetic for balances.
        cur.execute(  # => account table exists, one starting row
            "CREATE TABLE account(id INTEGER PRIMARY KEY, balance NUMERIC(10,2) NOT NULL)"
        )
        cur.execute("INSERT INTO account(id, balance) VALUES (1, 500.00)")
    # psycopg opens an implicit transaction on the FIRST statement of a connection --
    # nothing setup() does is visible to session_b until this commit() runs.
    conn.commit()  # => makes the seed data visible to BOTH sessions opened below


# main() orchestrates the whole three-act demo: acquire the lock, prove the
# second session blocks, release the lock, prove the second session then succeeds.
def main() -> None:  # => the script's entry point
    # Each psycopg.connect() call opens a genuinely separate server-side backend
    # process -- PostgreSQL's per-connection process model is what makes row locks
    # visible/enforceable across the two sessions, not just two Python objects.
    session_a = psycopg.connect(DSN)  # => session A: will hold the row lock
    session_b = psycopg.connect(DSN)  # => session B: will try to acquire the same lock
    setup(session_a)  # => seed once, using session A's connection

    # session_a's SELECT ... FOR UPDATE runs and its enclosing transaction is left
    # OPEN (no commit yet) -- the row lock it acquires stays held for as long as
    # this transaction remains open, which session_b will run into next.
    with session_a.cursor() as cur_a:
        cur_a.execute("SELECT id, balance FROM account WHERE id = 1 FOR UPDATE")
        # => FOR UPDATE (co-16) takes an exclusive ROW lock on id=1 -- held until
        # => session A commits or rolls back -- the transaction is still open here
        # fetchone() retrieves the single locked row -- FOR UPDATE does not change what
        # is fetched, only what lock is held on the underlying row while it is.
        row = cur_a.fetchone()
        print(
            f"Session A locked row: {row}"
        )  # => Output: Session A locked row: (1, Decimal('500.00'))

    # session_b is a WHOLLY separate connection/transaction -- it has no visibility
    # into session_a's uncommitted lock beyond being blocked BY it.
    with session_b.cursor() as cur_b:
        # lock_timeout is a per-session setting -- it does not affect session_a or any
        # other connection, only how long THIS session will wait for a blocked lock.
        cur_b.execute("SET lock_timeout = '500ms'")
        # => without a timeout, session B would hang until A commits or rolls back
        # Wrapping the blocking statement in try/except is what lets this script prove
        # the block happened programmatically instead of just hanging until manually killed.
        try:
            cur_b.execute("SELECT id, balance FROM account WHERE id = 1 FOR UPDATE")
            # => blocks because session A still holds the row lock -- after 500ms,
            # => lock_timeout cancels the wait and raises instead of hanging forever
            print("Session B acquired the lock (unexpected)")
        # LockNotAvailable maps directly to PostgreSQL's own 55P03 (lock_not_available)
        # error code -- lock_timeout is what turns an indefinite wait into this exception.
        except psycopg.errors.LockNotAvailable as exc:
            # => proves session B was genuinely BLOCKED by session A's open FOR UPDATE
            print(f"Session B blocked: {type(exc).__name__}")
            # => Output: Session B blocked: LockNotAvailable
        # Just like the aborted-transaction case in Example 20, a failed statement
        # leaves session_b's transaction unusable until an explicit ROLLBACK -- calling
        # rollback() here is what lets cur_b be reused for the next SELECT ... FOR UPDATE.
        session_b.rollback()  # => clears session B's failed statement before reusing it

    # Committing (rather than rolling back) session_a is what releases its FOR
    # UPDATE row lock -- PostgreSQL releases row locks at transaction END, whether
    # that end is COMMIT or ROLLBACK; the choice here only affects the DATA, not the lock release.
    session_a.commit()  # => releases session A's row lock -- session B can now proceed
    print(
        "Session A committed -- lock released"
    )  # => Output: Session A committed -- lock released

    # Now that session_a's transaction has ended, session_b's identical statement
    # succeeds immediately -- the SAME query, the SAME row, a completely different outcome.
    with session_b.cursor() as cur_b:
        cur_b.execute("SELECT id, balance FROM account WHERE id = 1 FOR UPDATE")
        # => the SAME statement that just failed now succeeds immediately -- no lock left
        row_b = cur_b.fetchone()
        print(
            f"Session B locked row: {row_b}"
        )  # => Output: Session B locked row: (1, Decimal('500.00'))
    # Committing session_b's own successful FOR UPDATE releases ITS row lock in
    # turn -- leaving no open lock behind once the script finishes.
    session_b.commit()  # => releases session B's own lock, tidy shutdown

    # Closing a connection with an open, uncommitted transaction would implicitly
    # roll it back -- both sessions already committed above, so close() here is pure cleanup.
    session_a.close()  # => always close what you open
    session_b.close()  # => both sessions cleaned up


# This guard is what pyright --strict's "no unused top-level code" expectations
# and ordinary Python script conventions both call for -- main() only runs when
# this file is executed directly, not when imported.
if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => entry point -- runs everything above when executed as a script
