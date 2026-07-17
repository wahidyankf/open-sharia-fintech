# pyright: strict
"""Capstone: anomaly_reproduce.py -- reproduces write skew (co-14) on employee.on_call.

Invariant: at least 1 Support employee (Leo id=14, Nancy id=15 -- seed.sql) stays
on_call at all times. Under REPEATABLE READ (co-13), two sessions each independently
see "2 on call" and each individually decide it is safe to go off -- neither sees the
OTHER's write, so BOTH commit, and the invariant ends up violated with 0 on call.
"""

import psycopg

DSN = "host=localhost port=55432 dbname=asqp user=asqp password=asqp"
# => connection string -- readers should substitute their own PostgreSQL 18 instance


def support_on_call_count(conn: psycopg.Connection) -> int:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT COUNT(*) FROM employee WHERE department_id = 4 AND on_call = TRUE"
        )
        row: tuple[int] | None = cur.fetchone()
        assert row is not None
        return row[0]


def reset_on_call_state(
    conn: psycopg.Connection,
) -> None:  # => resets state -- fully self-contained
    """Restore Leo (id=14) and Nancy (id=15) to on_call = TRUE, Oscar (id=16) to FALSE."""
    with conn.cursor() as cur:
        cur.execute("UPDATE employee SET on_call = TRUE WHERE id IN (14, 15)")
        cur.execute("UPDATE employee SET on_call = FALSE WHERE id = 16")
    conn.commit()


def main() -> None:  # => the script's entry point
    session_a = psycopg.connect(DSN)  # => session A: will take Leo (id=14) off call
    session_b = psycopg.connect(DSN)  # => session B: will take Nancy (id=15) off call
    reset_on_call_state(session_a)

    baseline = support_on_call_count(session_a)
    session_a.commit()  # => closes the implicit read-only transaction the SELECT above opened
    print(f"On-call count before either session starts: {baseline}")
    # => Output: On-call count before either session starts: 2

    with session_a.cursor() as cur_a, session_b.cursor() as cur_b:
        cur_a.execute("BEGIN ISOLATION LEVEL REPEATABLE READ")
        cur_b.execute("BEGIN ISOLATION LEVEL REPEATABLE READ")
        # => BOTH transactions open BEFORE either writes -- each gets its OWN snapshot
        # => showing 2 Support employees on call (co-13, co-14)

        cur_a.execute(
            "SELECT COUNT(*) FROM employee WHERE department_id = 4 AND on_call = TRUE"
        )
        seen_by_a = cur_a.fetchone()
        print(f"Session A sees on-call count: {seen_by_a}")
        # => Output: Session A sees on-call count: (2,)

        cur_b.execute(
            "SELECT COUNT(*) FROM employee WHERE department_id = 4 AND on_call = TRUE"
        )
        seen_by_b = cur_b.fetchone()
        print(f"Session B sees on-call count: {seen_by_b}")
        # => Output: Session B sees on-call count: (2,)
        # => BOTH sessions independently conclude "2 on call, safe for MY engineer to go off"

        cur_a.execute("UPDATE employee SET on_call = FALSE WHERE id = 14")
        session_a.commit()
        print("Session A took Leo (id=14) off call and committed")

        cur_b.execute("UPDATE employee SET on_call = FALSE WHERE id = 15")
        session_b.commit()
        # => REPEATABLE READ only detects conflicts on the SAME row -- session A wrote
        # => id=14, session B wrote id=15 -- NO row overlap, so NO conflict is detected,
        # => and BOTH commits succeed (co-13) despite violating the shared invariant
        print(
            "Session B took Nancy (id=15) off call and committed (no conflict detected)"
        )

    final = support_on_call_count(session_a)
    print(f"Final on-call count: {final}")
    # => Output: Final on-call count: 0
    print(f"Invariant (at least 1 on call) violated: {final == 0}")
    # => Output: Invariant (at least 1 on call) violated: True
    # => classic write skew: two disjoint writes, each individually valid against its
    # => own stale snapshot, together break an invariant neither write touches alone

    session_a.close()  # => always close what you open
    session_b.close()  # => both sessions cleaned up


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => entry point -- runs everything above when executed as a script
