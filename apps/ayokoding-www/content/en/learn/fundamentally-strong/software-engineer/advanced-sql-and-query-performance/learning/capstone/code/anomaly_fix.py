# pyright: strict
"""Capstone: anomaly_fix.py -- resolves the write skew anomaly_reproduce.py demonstrated,
using SERIALIZABLE (co-13, co-15) instead of REPEATABLE READ, plus an application-level
retry loop for the 40001 SerializationFailure PostgreSQL's SSI raises.

The SAME 2 disjoint UPDATEs interleave exactly like anomaly_reproduce.py: session A takes
Leo (id=14) off call, session B takes Nancy (id=15) off call, both starting from a "2 on
call" snapshot. Under SERIALIZABLE, PostgreSQL's Serializable Snapshot Isolation detects
the dangerous read-write dependency between the two transactions and aborts the SECOND
one to commit (co-15) instead of silently letting both through. The retry then re-reads
FRESH state and correctly refuses, because taking the last on-call engineer off would
drop the count to 0.
"""

import psycopg
from psycopg import errors

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


def retry_take_off_call(employee_id: int, label: str) -> str:
    # A FRESH connection + FRESH SERIALIZABLE transaction -- re-reading current state is
    # the whole point of a retry; a stale in-memory count would just repeat the same bug.
    conn = psycopg.connect(DSN)
    with conn.cursor() as cur:
        cur.execute("BEGIN ISOLATION LEVEL SERIALIZABLE")
        current_count = support_on_call_count(conn)
        print(f"  {label} re-reads on-call count: {current_count}")
        if current_count <= 1:
            # => the APPLICATION-LEVEL guard (co-14): going off call now would violate
            # => "at least 1 on call" -- refuse, using data THIS transaction can trust
            conn.rollback()
            conn.close()
            return "refused (would violate invariant)"
        cur.execute("UPDATE employee SET on_call = FALSE WHERE id = %s", (employee_id,))
        conn.commit()
    conn.close()
    return "went off call"


def main() -> None:  # => the script's entry point
    setup_conn = psycopg.connect(DSN)
    reset_on_call_state(setup_conn)
    baseline = support_on_call_count(setup_conn)
    print(f"On-call count before either session starts: {baseline}")
    # => Output: On-call count before either session starts: 2
    setup_conn.close()

    session_a = psycopg.connect(DSN)  # => session A: will take Leo (id=14) off call
    session_b = psycopg.connect(DSN)  # => session B: will take Nancy (id=15) off call

    serialization_failed = False
    with session_a.cursor() as cur_a, session_b.cursor() as cur_b:
        cur_a.execute("BEGIN ISOLATION LEVEL SERIALIZABLE")
        cur_b.execute("BEGIN ISOLATION LEVEL SERIALIZABLE")
        # => BOTH transactions open BEFORE either writes -- the SAME race
        # => anomaly_reproduce.py ran, now under SERIALIZABLE instead of REPEATABLE READ

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

        cur_a.execute("UPDATE employee SET on_call = FALSE WHERE id = 14")
        session_a.commit()
        print("Session A took Leo (id=14) off call and committed")

        try:
            cur_b.execute("UPDATE employee SET on_call = FALSE WHERE id = 15")
            session_b.commit()
            print("Session B took Nancy (id=15) off call and committed (unexpected)")
        except errors.SerializationFailure as exc:
            # => co-15 -- SSI detected the dangerous rw-dependency BETWEEN session A's
            # => write and session B's earlier read, and aborted session B rather than
            # => let both commits through the way REPEATABLE READ just did
            serialization_failed = True
            print(f"Session B got SerializationFailure: {exc.sqlstate}")
            session_b.rollback()

    session_a.close()  # => always close what you open
    session_b.close()

    if serialization_failed:
        result = retry_take_off_call(15, "Session B retry")
        print(f"Session B retry result: {result}")
        # => Output: Session B retry result: refused (would violate invariant)

    final_conn = psycopg.connect(DSN)
    final = support_on_call_count(final_conn)
    print(f"Final on-call count: {final}")
    # => Output: Final on-call count: 1
    print(f"Invariant (at least 1 on call) preserved: {final >= 1}")
    # => Output: Invariant (at least 1 on call) preserved: True
    final_conn.close()


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => entry point -- runs everything above when executed as a script
