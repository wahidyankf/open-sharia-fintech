# pyright: strict
# Same strict-typing baseline as Examples 57-59 -- no extra stub configuration
# needed beyond the installed psycopg package.
"""Example 60: Serialization Failure, Retry."""

# psycopg.errors.SerializationFailure below is the specific exception SSI
# raises -- no extra import needed since it lives on the psycopg module itself.
import psycopg

DSN = "host=localhost port=55432 dbname=asqp user=asqp password=asqp"
# => connection string -- readers should substitute their own PostgreSQL 18 instance


# Identical schema and seed data to Example 59's write-skew scenario -- the
# ONLY variable this example changes is the isolation level, from REPEATABLE
# READ to SERIALIZABLE, to show the SAME race handled correctly.
def setup(conn: psycopg.Connection) -> None:  # => resets state -- fully self-contained
    """Create the SAME two on-call doctors as Example 59, under SERIALIZABLE this time."""
    with conn.cursor() as cur:
        cur.execute("SET client_min_messages TO WARNING")
        # An idempotent DROP/CREATE reset, same as every other example in this
        # topic -- lets this script run repeatedly against the same database.
        cur.execute("DROP TABLE IF EXISTS doctor_on_call CASCADE")
        cur.execute(
            "CREATE TABLE doctor_on_call(id INTEGER PRIMARY KEY, name TEXT NOT NULL, "
            "on_call BOOLEAN NOT NULL)"
        )
        cur.execute(
            "INSERT INTO doctor_on_call(id, name, on_call) VALUES "
            "(1, 'Dr. Alice', TRUE), (2, 'Dr. Bob', TRUE)"
        )
    conn.commit()


# main() replays Example 59's exact interleaving under SERIALIZABLE -- watch
# for where session B's commit now FAILS instead of silently succeeding, and
# how the retry loop recovers correctly.
def main() -> None:  # => the script's entry point
    # Two separate connections model two independent application server
    # processes racing to update the same shared invariant concurrently.
    session_a = psycopg.connect(
        DSN
    )  # => session A: takes Dr. Alice off call, commits first
    session_b = psycopg.connect(
        DSN
    )  # => session B: tries Dr. Bob, hits the SAME race as Example 59
    setup(session_a)

    with session_a.cursor() as cur_a, session_b.cursor() as cur_b:
        cur_a.execute("BEGIN ISOLATION LEVEL SERIALIZABLE")
        cur_b.execute("BEGIN ISOLATION LEVEL SERIALIZABLE")
        # => SERIALIZABLE (co-15), not REPEATABLE READ -- PostgreSQL's SSI tracks
        # => read/write dependencies BETWEEN transactions, not just row-level conflicts

        # Both sessions read the SAME invariant-satisfying snapshot -- from each
        # session's own point of view, taking their doctor off call still looks safe.
        cur_a.execute("SELECT COUNT(*) FROM doctor_on_call WHERE on_call = TRUE")
        cur_a.fetchone()
        cur_b.execute("SELECT COUNT(*) FROM doctor_on_call WHERE on_call = TRUE")
        cur_b.fetchone()
        # => same stale-read setup as Example 59 -- both sessions see 2 on call

        # Session A commits FIRST and cleanly -- SSI never blocks the transaction
        # that happens to finish first; only the SECOND, dependency-violating
        # transaction pays the cost.
        cur_a.execute("UPDATE doctor_on_call SET on_call = FALSE WHERE id = 1")
        session_a.commit()
        # This commit succeeds unconditionally -- SSI has nothing to check
        # against yet, since session B has not written anything.
        print("Session A took Dr. Alice off call and committed")

        # This try/except is the production pattern for SERIALIZABLE: always wrap
        # the commit (or the whole transaction) so a SerializationFailure can be
        # caught and retried, instead of propagating as an unhandled crash.
        try:
            cur_b.execute("UPDATE doctor_on_call SET on_call = FALSE WHERE id = 2")
            session_b.commit()
            # This line only prints if SSI somehow failed to detect the conflict --
            # it exists as a defensive assertion-by-print, not an expected outcome.
            print("Session B committed (unexpected)")
        except psycopg.errors.SerializationFailure as exc:
            # => SSI (co-15) detected the SAME dangerous read/write pattern that
            # => slipped through under REPEATABLE READ in Example 59 -- it aborts
            # => ONE of the two transactions rather than let the invariant break
            print(f"Session B serialization failure: {type(exc).__name__}")
            # => Output: Session B serialization failure: SerializationFailure
            # A rollback() is MANDATORY after any error on a psycopg connection --
            # the transaction is left in an aborted state until explicitly rolled back,
            # and any further query on it would raise InFailedSqlTransaction.
            session_b.rollback()

            # The RETRY (co-15): re-run session B's transaction from scratch against
            # FRESH data -- this is the mandatory pattern for SERIALIZABLE in production.
            with session_b.cursor() as cur_retry:
                cur_retry.execute("BEGIN ISOLATION LEVEL SERIALIZABLE")
                # A brand-new BEGIN takes a brand-new snapshot -- this retry sees the
                # world AFTER session A's commit, not the stale pre-commit view that
                # caused the original conflict.
                cur_retry.execute(
                    "SELECT COUNT(*) FROM doctor_on_call WHERE on_call = TRUE"
                )
                retry_count = cur_retry.fetchone()
                print(f"Session B retry sees on-call count: {retry_count}")
                # => Output: Session B retry sees on-call count: (1,)
                # => the retry sees Alice's commit -- correctly refuses to take Bob off too
                # The type checker cannot infer that a COUNT(*) query always
                # returns exactly one row -- this assert narrows Optional[Any] to
                # a concrete tuple for the subscript access on the next line.
                assert retry_count is not None
                # Business-rule check runs INSIDE the retry, against fresh data -- this
                # is what actually prevents the invariant violation; SERIALIZABLE only
                # guarantees a CONSISTENT view to check against, not the check itself.
                if retry_count[0] <= 1:
                    print("Session B retry: refusing -- would violate invariant")
                    session_b.rollback()

    # A fresh, uncontested read after both sessions have resolved -- this confirms
    # the FINAL committed state of the database, not either session's snapshot.
    with session_a.cursor() as cur_check:
        cur_check.execute("SELECT COUNT(*) FROM doctor_on_call WHERE on_call = TRUE")
        final_count = cur_check.fetchone()
        print(f"Final on-call count: {final_count}")
        # => Output: Final on-call count: (1,)
        # => the invariant HOLDS this time -- SERIALIZABLE plus a retry loop is what
        # => Example 59's REPEATABLE READ version needed and did not have

    # Both connections are cleaned up regardless of which retry branch ran --
    # no leaked connections whether the SSI conflict fired or not.
    session_a.close()  # => always close what you open
    session_b.close()  # => both sessions cleaned up


# The trade-off SERIALIZABLE makes explicit: strong correctness guarantees in
# exchange for application code that MUST be prepared to retry -- unlike
# REPEATABLE READ or READ COMMITTED, which never raise this class of error.
if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => entry point -- runs everything above when executed as a script
