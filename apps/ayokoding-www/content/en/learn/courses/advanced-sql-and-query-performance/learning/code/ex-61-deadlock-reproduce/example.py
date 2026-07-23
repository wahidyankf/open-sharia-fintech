# pyright: strict
# Same strict-typing baseline as Examples 57-60 -- no extra stub configuration
# needed beyond the installed psycopg package.
"""Example 61: Deadlock, Reproduce."""

# threading.Barrier is the key ingredient that makes this a GENUINE deadlock
# demo rather than a race that only sometimes reproduces -- it forces both
# worker threads to hold their first lock simultaneously before either
# requests the second, guaranteeing the circular wait every single run.
import threading

import psycopg

DSN = "host=localhost port=55432 dbname=asqp user=asqp password=asqp"
# => connection string -- readers should substitute their own PostgreSQL 18 instance


# Two accounts, each about to be locked by two DIFFERENT transactions in
# OPPOSITE order -- that opposite ordering is the entire cause of the deadlock
# below; same-order locking would never deadlock, only serialize.
def setup() -> None:  # => resets state -- fully self-contained
    """Create two account rows -- each thread below locks them in OPPOSITE order."""
    conn = psycopg.connect(DSN)
    with conn.cursor() as cur:
        cur.execute("SET client_min_messages TO WARNING")
        # Same idempotent reset pattern as every other example in this topic.
        cur.execute("DROP TABLE IF EXISTS account CASCADE")
        cur.execute(
            "CREATE TABLE account(id INTEGER PRIMARY KEY, balance NUMERIC(10,2) NOT NULL)"
        )
        # Both accounts start at the same balance -- the actual amounts moved (10
        # and 5 below) are arbitrary; only the LOCK ORDER matters for this demo.
        cur.execute("INSERT INTO account(id, balance) VALUES (1, 500.00), (2, 500.00)")
    conn.commit()
    conn.close()


# worker_a and worker_b run on SEPARATE threads (see main()) so their UPDATE
# statements genuinely interleave at the database level -- this is the only
# example in this topic that uses real OS threads instead of sequential
# cursor calls, because deadlocks require true concurrency to reproduce.
def worker_a(barrier: threading.Barrier, results: dict[str, str]) -> None:
    # => session A: locks id=1 FIRST, then requests id=2 -- opposite order to worker_b
    conn = psycopg.connect(DSN)
    with conn.cursor() as cur:
        cur.execute("BEGIN")
        # This UPDATE acquires a row-level lock on id=1 and HOLDS it until commit
        # or rollback -- Postgres's default row-level locking is exactly what makes
        # two opposite-order UPDATEs capable of deadlocking.
        cur.execute("UPDATE account SET balance = balance - 10 WHERE id = 1")
        barrier.wait()  # => waits for worker_b to also hold ITS first lock -- guarantees the cycle
        try:
            # At this point worker_b already holds id=2's lock (via the barrier
            # above) -- this UPDATE blocks waiting for id=2, while worker_b is
            # simultaneously blocked waiting for id=1: a genuine circular wait.
            cur.execute("UPDATE account SET balance = balance + 10 WHERE id = 2")
            conn.commit()
            # A clean commit here means worker_a was NOT chosen as the deadlock
            # victim -- its full UPDATE sequence succeeded end to end.
            results["a"] = "committed"
        except psycopg.errors.DeadlockDetected as exc:
            # PostgreSQL guarantees ONE side of a deadlock always gets this exception
            # -- the other side's blocked UPDATE then completes normally once the
            # chosen victim's lock is released by the rollback below.
            conn.rollback()
            results["a"] = f"deadlock: {type(exc).__name__}"
    conn.close()


# worker_b is the mirror image of worker_a: SAME two rows, OPPOSITE lock order
# (id=2 first, then id=1) -- the asymmetry between the two workers is the
# entire mechanism that produces the circular wait.
def worker_b(barrier: threading.Barrier, results: dict[str, str]) -> None:
    # => session B: locks id=2 FIRST, then requests id=1 -- the REVERSE of worker_a,
    # => which is exactly what creates the circular wait a deadlock needs
    conn = psycopg.connect(DSN)
    with conn.cursor() as cur:
        cur.execute("BEGIN")
        # Locks id=2 first -- worker_a is simultaneously locking id=1 first, so by
        # the time both reach their barrier.wait(), each side holds exactly the
        # ONE row the other side needs next.
        cur.execute("UPDATE account SET balance = balance - 5 WHERE id = 2")
        barrier.wait()  # => waits for worker_a to also hold ITS first lock -- guarantees the cycle
        try:
            # Requesting id=1 here while worker_a holds it (and is itself waiting
            # on id=2) closes the cycle -- Postgres's deadlock detector will find
            # this within one deadlock_timeout interval (1s by default).
            cur.execute("UPDATE account SET balance = balance + 5 WHERE id = 1")
            conn.commit()
            results["b"] = "committed"
        except psycopg.errors.DeadlockDetected as exc:
            conn.rollback()
            results["b"] = f"deadlock: {type(exc).__name__}"
    conn.close()


# main() orchestrates the barrier synchronization and reports which of the two
# threads PostgreSQL chose as the deadlock victim -- that choice is
# nondeterministic between runs, but exactly one side always loses.
def main() -> None:  # => the script's entry point
    setup()
    barrier = threading.Barrier(2)  # => real threads, not sequential calls -- a
    # => genuine deadlock needs BOTH sides blocked on each other AT THE SAME TIME
    results: dict[str, str] = {}
    # results is shared, mutable state written by both threads -- safe here
    # because each thread writes only its own key ('a' or 'b'), never the other's.
    thread_a = threading.Thread(target=worker_a, args=(barrier, results))
    thread_b = threading.Thread(target=worker_b, args=(barrier, results))
    # Both threads start before either finishes -- this is what allows them to
    # race toward their respective barrier.wait() calls concurrently.
    thread_a.start()
    thread_b.start()
    # join() blocks main() until BOTH worker threads have fully finished --
    # results['a'] and results['b'] are guaranteed populated by this point.
    # Both mitigations -- consistent lock ordering AND a DeadlockDetected retry
    # handler -- are what production code needs; this example only demonstrates
    # the failure mode in isolation.
    thread_a.join()
    thread_b.join()
    # => PostgreSQL's own deadlock detector (checks every deadlock_timeout, 1s by
    # => default) finds the id=1<->id=2 cycle and aborts EXACTLY ONE of the two
    print(f"Session A result: {results['a']}")
    print(f"Session B result: {results['b']}")
    # => Output (order may vary which side is chosen as victim):
    # => Session A result: committed
    # => Session B result: deadlock: DeadlockDetected


# Application-level lessons this example teaches: always acquire locks in a
# CONSISTENT global order across the whole codebase to avoid deadlocks
# entirely, and always be prepared to catch DeadlockDetected and retry when a
# consistent order is not achievable.
if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => entry point -- runs everything above when executed as a script
