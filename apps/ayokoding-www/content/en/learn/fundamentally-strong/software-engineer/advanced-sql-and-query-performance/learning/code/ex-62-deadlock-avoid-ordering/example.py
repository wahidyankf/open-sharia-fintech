# pyright: strict
# Same strict-typing baseline as Example 61 -- no extra stub configuration
# needed beyond the installed psycopg package.
"""Example 62: Deadlock, Avoid via Consistent Ordering."""

# threading is still needed to run both workers concurrently -- the FIX here
# is not removing concurrency, it is removing the opposite lock ORDER that
# made Example 61's concurrency dangerous.
import threading

import psycopg

DSN = "host=localhost port=55432 dbname=asqp user=asqp password=asqp"
# => connection string -- readers should substitute their own PostgreSQL 18 instance


# Identical schema and starting balances to Example 61 -- the ONLY difference
# between these two examples is the lock order inside worker_b, isolating that
# single variable as the cause of (and cure for) the deadlock.
def setup() -> None:  # => resets state -- fully self-contained
    """Create the SAME two account rows as Example 61, for a fair comparison."""
    conn = psycopg.connect(DSN)
    with conn.cursor() as cur:
        cur.execute("SET client_min_messages TO WARNING")
        # Same idempotent reset pattern used throughout this topic.
        cur.execute("DROP TABLE IF EXISTS account CASCADE")
        cur.execute(
            "CREATE TABLE account(id INTEGER PRIMARY KEY, balance NUMERIC(10,2) NOT NULL)"
        )
        # Same starting balances as Example 61 -- only the LOCK ORDER changes below.
        cur.execute("INSERT INTO account(id, balance) VALUES (1, 500.00), (2, 500.00)")
    conn.commit()
    conn.close()


# worker_a is UNCHANGED from Example 61's worker_a -- it always locked id=1
# before id=2, so it never needed fixing; worker_b below is the one that
# changes.
def worker_a(results: dict[str, str]) -> None:
    # => session A: locks id=1, THEN id=2 -- ascending order
    conn = psycopg.connect(DSN)
    with conn.cursor() as cur:
        cur.execute("BEGIN")
        # Note this version has NO threading.Barrier -- consistent ordering makes
        # the deadlock impossible regardless of exact timing, so there is nothing
        # left to deliberately synchronize.
        # id=1 first -- worker_a's order was already correct in Example 61 and
        # stays unchanged here.
        cur.execute("UPDATE account SET balance = balance - 10 WHERE id = 1")
        cur.execute("UPDATE account SET balance = balance + 10 WHERE id = 2")
        conn.commit()
        results["a"] = "committed"
    conn.close()


# THIS is the fixed function -- compare its lock order (id=1, then id=2) to
# Example 61's worker_b (id=2, then id=1). That single swap is the entire fix.
def worker_b(results: dict[str, str]) -> None:
    # => session B: ALSO locks id=1, THEN id=2 -- the FIX (co-17): both sessions
    # => now agree on a single global lock order, so there is no cycle to form.
    # => Whichever thread reaches id=1 first simply makes the OTHER wait its turn
    conn = psycopg.connect(DSN)
    with conn.cursor() as cur:
        cur.execute("BEGIN")
        # If id=1 is currently locked by worker_a, this UPDATE simply BLOCKS until
        # worker_a's transaction ends -- a normal wait, never a circular one,
        # because BOTH workers approach id=1 before id=2.
        # id=1 first here too -- this is the ONE line that differs from
        # Example 61's worker_b, which locked id=2 first instead.
        cur.execute("UPDATE account SET balance = balance - 5 WHERE id = 1")
        cur.execute("UPDATE account SET balance = balance + 5 WHERE id = 2")
        conn.commit()
        results["b"] = "committed"
    conn.close()


# main() runs the two workers concurrently exactly like Example 61 -- same
# threading pattern, same shared results dict -- to isolate lock ordering as
# the only variable that changed between the two examples.
def main() -> None:  # => the script's entry point
    setup()
    results: dict[str, str] = {}
    # No threading.Barrier import or usage anywhere in this file -- Example
    # 61 needed one to FORCE the race; this fix needs no such choreography.
    thread_a = threading.Thread(target=worker_a, args=(results,))
    thread_b = threading.Thread(target=worker_b, args=(results,))
    # No barrier.wait() here (unlike Example 61) -- there is no specific
    # interleaving that needs to be forced; the fix holds under ANY timing.
    thread_a.start()
    thread_b.start()
    thread_a.join()
    # In production, this discipline is usually enforced by always locking rows
    # in a stable key order (e.g. ascending primary key), never in whatever order
    # a particular code path happens to touch them.
    thread_b.join()
    # => NO deadlock this time: one thread blocks briefly waiting for id=1's row
    # => lock to release, then proceeds normally -- ordinary serialization, not a cycle
    print(f"Session A result: {results['a']}")
    print(f"Session B result: {results['b']}")
    # => Output: Session A result: committed
    # => Output: Session B result: committed
    # => BOTH commit -- consistent lock ordering across ALL callers eliminates deadlocks
    # => by construction, without needing PostgreSQL's deadlock detector at all


# Consistent lock ordering is a DISCIPLINE, not a database feature -- it must be
# enforced across every code path that touches these two rows, since a single
# forgotten caller reverting to the old order reintroduces Example 61's bug.
if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => entry point -- runs everything above when executed as a script
