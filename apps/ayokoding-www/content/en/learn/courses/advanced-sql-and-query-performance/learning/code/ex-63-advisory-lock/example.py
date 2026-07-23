# pyright: strict
# Same strict-typing baseline as every other psycopg example in this topic.
"""Example 63: Advisory Lock."""

# psycopg alone is enough here -- advisory locks are plain SQL function calls
# (pg_try_advisory_lock / pg_advisory_unlock), not a distinct client-side API.
import psycopg

DSN = "host=localhost port=55432 dbname=asqp user=asqp password=asqp"
# => connection string -- readers should substitute their own PostgreSQL 18 instance

LOCK_KEY = 424242  # => an arbitrary application-chosen BIGINT -- no table row backs this at all


# This example has no setup() function at all -- unlike every locking example
# so far (Examples 26, 57-62), advisory locks coordinate application logic
# directly, with no table or row involved that would need seeding.
def main() -> None:  # => the script's entry point
    session_a = psycopg.connect(DSN)  # => session A: holds an advisory lock (co-16)
    session_b = psycopg.connect(
        DSN
    )  # => session B: tries to acquire the SAME advisory lock

    # Typical uses for advisory locks: serializing a scheduled job across
    # multiple app server instances, or guarding a critical section that has no
    # natural database row to attach a FOR UPDATE lock to.
    with session_a.cursor() as cur_a:
        cur_a.execute("SELECT pg_try_advisory_lock(%s)", (LOCK_KEY,))
        acquired_a = cur_a.fetchone()
        print(f"Session A pg_try_advisory_lock: {acquired_a}")
        # => Output: Session A pg_try_advisory_lock: (True,)
        # => an ADVISORY lock (co-16) is NOT tied to any row or table -- it exists
        # => purely at the session level, identified by an application-chosen integer key

        with session_b.cursor() as cur_b:
            cur_b.execute("SELECT pg_try_advisory_lock(%s)", (LOCK_KEY,))
            # => pg_try_advisory_lock is NON-BLOCKING -- returns immediately with
            # => false rather than waiting, unlike FOR UPDATE in Example 26
            acquired_b = cur_b.fetchone()
            print(f"Session B pg_try_advisory_lock: {acquired_b}")
            # => Output: Session B pg_try_advisory_lock: (False,)
            # => the SAME key is already held by session A -- session B is refused, not blocked

        # Releasing is EXPLICIT -- unlike a row lock, which Postgres automatically
        # releases at transaction end, a session-level advisory lock is held until
        # this function is called or the connection itself closes.
        cur_a.execute("SELECT pg_advisory_unlock(%s)", (LOCK_KEY,))
        released = cur_a.fetchone()
        print(f"Session A pg_advisory_unlock: {released}")
        # => Output: Session A pg_advisory_unlock: (True,)

    # Only after the unlock above is the key genuinely free -- this retry
    # exercises that exact handoff, proving the lock was truly released rather
    # than merely appearing to succeed.
    with session_b.cursor() as cur_b:
        cur_b.execute("SELECT pg_try_advisory_lock(%s)", (LOCK_KEY,))
        acquired_b_retry = cur_b.fetchone()
        print(f"Session B retry pg_try_advisory_lock: {acquired_b_retry}")
        # => Output: Session B retry pg_try_advisory_lock: (True,)
        # => now free -- session B acquires it immediately once A released it
        cur_b.execute("SELECT pg_advisory_unlock(%s)", (LOCK_KEY,))
        cur_b.fetchone()

    session_a.close()  # => always close what you open
    session_b.close()  # => both sessions cleaned up


# pg_try_advisory_lock has a BLOCKING counterpart, pg_advisory_lock, which
# waits indefinitely instead of returning false -- choose the try/non-blocking
# form whenever the caller needs to do something else on refusal.
if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => entry point -- runs everything above when executed as a script
