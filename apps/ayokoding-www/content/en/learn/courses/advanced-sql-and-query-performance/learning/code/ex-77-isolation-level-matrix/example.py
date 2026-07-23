# pyright: strict
# Same strict-typing baseline as Examples 57-60 -- no extra stub configuration
# needed beyond the installed psycopg package.
"""Example 77: Isolation Level Matrix."""

import psycopg

DSN = "host=localhost port=55432 dbname=asqp user=asqp password=asqp"
# => connection string -- readers should substitute their own PostgreSQL 18 instance

ISOLATION_LEVELS = ["READ COMMITTED", "REPEATABLE READ", "SERIALIZABLE"]
# => the SAME non-repeatable-read workload (Examples 27 and 57) run at ALL THREE
# => levels (co-13) -- this example is the direct side-by-side comparison


# reset_account() is called once per isolation level via main()'s loop -- each
# level gets a FRESH, identical starting balance so the three runs are
# genuinely comparable rather than accumulating state across iterations.
def reset_account(
    conn: psycopg.Connection,
) -> None:  # => resets state before EACH level's run
    with conn.cursor() as cur:
        cur.execute("SET client_min_messages TO WARNING")
        cur.execute("DROP TABLE IF EXISTS account CASCADE")
        cur.execute(
            "CREATE TABLE account(id INTEGER PRIMARY KEY, balance NUMERIC(10,2) NOT NULL)"
        )
        # Same starting balance and identical interleaving to Examples 27 and 57 --
        # this run_at_level() function is deliberately their COMMON logic, generalized.
        cur.execute("INSERT INTO account(id, balance) VALUES (1, 500.00)")
    conn.commit()


# This single function replays the EXACT non-repeatable-read interleaving used
# in Examples 27 (READ COMMITTED) and 57 (REPEATABLE READ), parameterized by
# isolation level -- one function, three data points in the matrix.
def run_at_level(level: str) -> bool:
    # => returns True if the anomaly (co-14) was PERMITTED (second read differs
    # => from the first), False if the isolation level PREVENTED it
    # Two connections per level-run, exactly like Examples 27, 57, 58, and 59 --
    # this function is those examples' shared skeleton, made reusable.
    session_a = psycopg.connect(DSN)
    session_b = psycopg.connect(DSN)
    reset_account(session_a)

    with session_a.cursor() as cur_a:
        # psycopg's execute() requires a LiteralString for safety (no dynamic
        # SQL injection risk) -- an if/elif over the 3 known constants keeps
        # every call a true string literal instead of an f-string interpolation.
        if level == "READ COMMITTED":
            cur_a.execute("BEGIN ISOLATION LEVEL READ COMMITTED")
        elif level == "REPEATABLE READ":
            cur_a.execute("BEGIN ISOLATION LEVEL REPEATABLE READ")
        else:
            # The only remaining possibility, given ISOLATION_LEVELS above, is
            # SERIALIZABLE -- pyright cannot infer this from the string type alone,
            # so the else branch stands in for that final case explicitly.
            cur_a.execute("BEGIN ISOLATION LEVEL SERIALIZABLE")
        # This first read establishes the BASELINE value every level starts from
        # -- 500.00, before session B's concurrent write below.
        cur_a.execute("SELECT balance FROM account WHERE id = 1")
        first_read = cur_a.fetchone()

        # Session B always runs and commits under its OWN default isolation
        # (READ COMMITTED) -- what varies across the matrix is session A's level,
        # not session B's.
        with session_b.cursor() as cur_b:
            cur_b.execute("UPDATE account SET balance = 400.00 WHERE id = 1")
            session_b.commit()

        # The SAME query, re-run inside the SAME still-open transaction -- whether
        # this now returns 400.00 or still 500.00 is exactly what distinguishes
        # the three isolation levels in this matrix.
        cur_a.execute("SELECT balance FROM account WHERE id = 1")
        second_read = cur_a.fetchone()
        session_a.commit()

    session_a.close()  # => always close what you open
    session_b.close()  # => both sessions cleaned up
    return first_read != second_read


# main() drives run_at_level() across all three ISOLATION_LEVELS and prints a
# compact, aligned table -- the format makes the READ COMMITTED vs the other
# two levels' contrast immediately visible at a glance.
def main() -> None:  # => the script's entry point
    print(f"{'Isolation Level':<20} {'Anomaly Permitted?':<20}")
    # A dashed divider matching the header's 40-character width -- purely
    # cosmetic, but makes the printed table easier to scan visually.
    print("-" * 40)
    for level in ISOLATION_LEVELS:
        anomaly_permitted = run_at_level(level)
        print(f"{level:<20} {str(anomaly_permitted):<20}")
        # => Output rows:
        # => READ COMMITTED      True   -- Example 27: sees B's mid-transaction commit
        # => REPEATABLE READ     False  -- Example 57: snapshot fixed at BEGIN, never moves
        # => SERIALIZABLE        False  -- SSI is snapshot-based too (co-13): SAME protection
        # =>                               against THIS specific anomaly as REPEATABLE READ


# This matrix format generalizes directly to other anomalies (phantom reads,
# write skew) covered separately in Examples 58-60 -- the same three-level
# comparison pattern applies to each one.
if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => entry point -- runs everything above when executed as a script
