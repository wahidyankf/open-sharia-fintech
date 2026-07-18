# pyright: strict
"""Capstone: n_plus_1.py -- diagnose the app-side N+1 (co-26) on the per-employee sales
report, then fix it with a single GROUP BY -- query count measured before and after,
against the SAME 250,000-row sales_event table tune_query.sql just tuned.
"""

import psycopg

DSN = "host=localhost port=55432 dbname=asqp user=asqp password=asqp"
# => connection string -- readers should substitute their own PostgreSQL 18 instance


def naive_per_employee_totals(conn: psycopg.Connection) -> dict[int, float]:
    # The N+1 pattern (co-26): ONE query lists the 18 employees, then a SEPARATE
    # round trip sums sales for EVERY single one of them -- 19 total queries.
    totals: dict[int, float] = {}
    query_count = 0
    with conn.cursor() as outer:
        outer.execute("SELECT id FROM employee ORDER BY id")
        query_count += 1  # => query 1: the employee id list
        employee_ids: list[tuple[int]] = outer.fetchall()
        for (employee_id,) in employee_ids:
            with conn.cursor() as inner:
                inner.execute(
                    "SELECT COALESCE(SUM(amount), 0) FROM sales_event WHERE employee_id = %s",
                    (employee_id,),
                )
                query_count += (
                    1  # => queries 2..19: one SEPARATE round trip per employee
                )
                row: tuple[float] | None = inner.fetchone()
                assert row is not None
                totals[employee_id] = float(row[0])
    print(f"Naive (N+1): {len(employee_ids)} employees, {query_count} total queries")
    # => Output: Naive (N+1): 18 employees, 19 total queries
    return totals


def fixed_group_by_totals(conn: psycopg.Connection) -> dict[int, float]:
    # The fix (co-26): ONE query joins employee to sales_event and groups by employee_id
    # -- every employee's total comes back in a SINGLE round trip, including the ones
    # with zero sales (LEFT JOIN + COALESCE, so nobody silently disappears from the report).
    query_count = 0
    with conn.cursor() as cur:
        cur.execute(
            "SELECT e.id, COALESCE(SUM(s.amount), 0) FROM employee e "
            "LEFT JOIN sales_event s ON s.employee_id = e.id "
            "GROUP BY e.id ORDER BY e.id"
        )
        query_count += 1  # => query 1: the ONLY query this version ever issues
        rows: list[tuple[int, float]] = cur.fetchall()
    totals: dict[int, float] = {
        employee_id: float(total) for employee_id, total in rows
    }
    print(f"Fixed (GROUP BY): {len(totals)} employees, {query_count} total queries")
    # => Output: Fixed (GROUP BY): 18 employees, 1 total queries
    return totals


def main() -> None:  # => the script's entry point
    conn = psycopg.connect(DSN)

    naive_totals = naive_per_employee_totals(conn)
    fixed_totals = fixed_group_by_totals(conn)

    assert naive_totals == fixed_totals
    # => co-26 -- the FIX changes query count, never the DATA -- both dicts agree exactly
    print(f"Totals match across both approaches: {naive_totals == fixed_totals}")
    # => Output: Totals match across both approaches: True

    conn.close()  # => always close what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => entry point -- runs everything above when executed as a script
