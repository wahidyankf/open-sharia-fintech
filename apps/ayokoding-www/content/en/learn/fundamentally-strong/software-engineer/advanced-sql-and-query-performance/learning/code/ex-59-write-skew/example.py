# pyright: strict
# Same strict-typing baseline as Examples 57-58 -- no extra stub configuration
# needed beyond the installed psycopg package.
"""Example 59: Write Skew."""

# No time import -- write skew is a CORRECTNESS anomaly, not a performance one.
import psycopg

DSN = "host=localhost port=55432 dbname=asqp user=asqp password=asqp"
# => connection string -- readers should substitute their own PostgreSQL 18 instance


# Write skew is the most subtle of the three anomalies in Examples 57-59: no
# single row is read-then-written twice (that would be a lock-detectable
# conflict) -- instead, TWO DIFFERENT rows are each modified based on a shared
# read of the OTHER row's state, silently breaking a cross-row invariant.
def setup(conn: psycopg.Connection) -> None:  # => resets state -- fully self-contained
    """Create two on-call doctors; the invariant is: at least one stays on call."""
    with conn.cursor() as cur:
        cur.execute("SET client_min_messages TO WARNING")
        cur.execute("DROP TABLE IF EXISTS doctor_on_call CASCADE")
        # on_call is a plain BOOLEAN -- the invariant this example breaks is an
        # APPLICATION-level rule ("never let both go off call"), not a database
        # CHECK constraint, which is exactly why the database cannot catch it alone.
        cur.execute(
            "CREATE TABLE doctor_on_call(id INTEGER PRIMARY KEY, name TEXT NOT NULL, "
            "on_call BOOLEAN NOT NULL)"
        )
        cur.execute(
            "INSERT INTO doctor_on_call(id, name, on_call) VALUES "
            "(1, 'Dr. Alice', TRUE), (2, 'Dr. Bob', TRUE)"
        )
        # => BOTH doctors start on call -- the invariant "at least 1 on call" holds
    conn.commit()


# main() interleaves two REPEATABLE READ transactions so that each one reads
# the invariant as satisfied, then independently makes a change that -- taken
# together -- violates it.
def main() -> None:  # => the script's entry point
    session_a = psycopg.connect(DSN)  # => session A: will take Dr. Alice off call
    session_b = psycopg.connect(DSN)  # => session B: will take Dr. Bob off call
    setup(session_a)

    # Both cursors share this one `with` statement purely for readability -- there is
    # no synchronization between them; each connection's transaction proceeds fully
    # independently on the Postgres server.
    with session_a.cursor() as cur_a, session_b.cursor() as cur_b:
        cur_a.execute("BEGIN ISOLATION LEVEL REPEATABLE READ")
        cur_b.execute("BEGIN ISOLATION LEVEL REPEATABLE READ")
        # => BOTH transactions open BEFORE either writes -- each gets its OWN
        # => snapshot showing 2 doctors on call (co-14, co-15)

        # Each session independently checks the SAME invariant against its own
        # snapshot -- neither has any way to know the OTHER session is about to
        # act on an overlapping decision.
        cur_a.execute("SELECT COUNT(*) FROM doctor_on_call WHERE on_call = TRUE")
        count_seen_by_a = cur_a.fetchone()
        print(f"Session A sees on-call count: {count_seen_by_a}")
        # => Output: Session A sees on-call count: (2,)

        cur_b.execute("SELECT COUNT(*) FROM doctor_on_call WHERE on_call = TRUE")
        count_seen_by_b = cur_b.fetchone()
        print(f"Session B sees on-call count: {count_seen_by_b}")
        # => Output: Session B sees on-call count: (2,)
        # => BOTH sessions independently conclude "2 on call, safe for MY doctor to go off"

        # Session A writes row id=1 -- this UPDATE touches ONLY Dr. Alice's row, never
        # id=2, so it cannot conflict with anything session B is about to do.
        cur_a.execute("UPDATE doctor_on_call SET on_call = FALSE WHERE id = 1")
        session_a.commit()
        print("Session A took Dr. Alice off call and committed")

        # Session B writes the DIFFERENT row id=2 -- Postgres's REPEATABLE READ
        # conflict detection only fires a serialization error when two transactions
        # touch the SAME row; disjoint writes to different rows sail through cleanly.
        cur_b.execute("UPDATE doctor_on_call SET on_call = FALSE WHERE id = 2")
        session_b.commit()
        # => REPEATABLE READ only detects conflicts on the SAME row -- session A
        # => wrote id=1, session B wrote id=2 -- NO row overlap, so NO conflict is
        # => detected, and BOTH commits succeed (co-15) despite violating the invariant
        print("Session B took Dr. Bob off call and committed (no conflict detected)")

    # A brand-new transaction (fresh snapshot) is required here to see the TRUE
    # current state -- the earlier snapshots inside session A and B's transactions
    # are now closed and would still show stale, pre-update data.
    with session_a.cursor() as cur_check:
        cur_check.execute("SELECT COUNT(*) FROM doctor_on_call WHERE on_call = TRUE")
        final_count = cur_check.fetchone()
        print(f"Final on-call count: {final_count}")
        # => Output: Final on-call count: (0,)
        # => the invariant "at least 1 on call" is now VIOLATED -- classic write skew:
        # => two disjoint writes, each individually valid against its own stale snapshot

    session_a.close()  # => always close what you open
    session_b.close()  # => both sessions cleaned up


# Preventing write skew (not shown here) requires either SERIALIZABLE isolation
# (which detects this exact dependency pattern) or an explicit SELECT ... FOR
# UPDATE / advisory lock that forces the two sessions to conflict on purpose.
# SERIALIZABLE would abort one of the two transactions with a serialization
# failure, forcing the application to retry -- a strictly stronger guarantee
# than REPEATABLE READ provides for this cross-row scenario.
if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => entry point -- runs everything above when executed as a script
