"""Example 83: Retention Policy, Drop Old Chunks."""  # => co-30,co-28: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import psycopg  # => co-30: psycopg, the official typed Python driver for PostgreSQL (TimescaleDB is a PG extension)


def seed_old_and_recent_data(conn: psycopg.Connection) -> None:  # => co-30: data straddling the 30-day retention window
    """Create a hypertable with 1-day chunks, then insert one point older than 30 days and one recent point."""  # => documents contract
    conn.execute("DROP TABLE IF EXISTS metrics_retention")  # => resets state -- this example is fully self-contained
    conn.execute("CREATE TABLE metrics_retention (ts TIMESTAMPTZ NOT NULL, value DOUBLE PRECISION NOT NULL)")  # => a plain table
    conn.execute(  # => co-30: a SMALL chunk_time_interval so the old and recent points land in DIFFERENT, separately droppable chunks
        "SELECT create_hypertable('metrics_retention', by_range('ts', INTERVAL '1 day'))"  # => 1-day chunks -- fine-grained enough to separate the two seeded points
    )  # => closes the execute() call -- metrics_retention is now a hypertable with 1-day chunks
    conn.execute(  # => co-30: 40 days old -- OUTSIDE the 30-day retention window, must be dropped
        "INSERT INTO metrics_retention (ts, value) VALUES (now() - INTERVAL '40 days', 1.0)"  # => co-30: lands in a chunk the retention policy WILL drop
    )  # => closes this one execute() call -- the old point now exists
    conn.execute(  # => co-30: recent -- INSIDE the 30-day retention window, must be RETAINED
        "INSERT INTO metrics_retention (ts, value) VALUES (now() - INTERVAL '1 hour', 2.0)"  # => co-30: lands in a chunk the retention policy must NOT drop
    )  # => closes this one execute() call -- the recent point now exists
    conn.commit()  # => makes both inserts durable before the retention policy runs


def add_and_run_retention_policy(conn: psycopg.Connection) -> None:  # => co-30: schedules AND immediately triggers the drop, rather than waiting on its own schedule
    """Add a 30-day retention policy, then manually run its background job once instead of waiting for its schedule."""  # => documents contract
    job_id_row = conn.execute(  # => co-30: add_retention_policy schedules a RECURRING background job -- it does not drop anything itself, synchronously
        "SELECT add_retention_policy('metrics_retention', drop_after => INTERVAL '30 days')"  # => co-30: schedules the drop -- anything older than 30 days becomes eligible
    ).fetchone()  # => this SELECT always returns exactly one row -- the newly-scheduled job's own id
    assert job_id_row is not None  # => confirms the scheduled job's id row genuinely came back
    job_id = job_id_row[0]  # => the single job id value this SELECT returns
    conn.commit()  # => makes the scheduled job durable before running it manually below
    conn.execute("CALL run_job(%s)", (job_id,))  # => co-30: manually triggers the job NOW, instead of waiting for its own background schedule -- parameterized, not an f-string, so psycopg's typed overload resolves cleanly
    conn.commit()  # => makes the job's chunk-drop effect durable


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    conn = psycopg.connect("host=localhost port=5433 dbname=nosqldb user=postgres password=nosqldb", autocommit=False)  # => connects to the local TimescaleDB Docker container
    conn.execute("CREATE EXTENSION IF NOT EXISTS timescaledb")  # => enables the extension, idempotent if already present
    conn.commit()  # => makes the extension creation durable before the hypertable conversion below

    seed_old_and_recent_data(conn)  # => co-30: seeds one 40-day-old point and one 1-hour-old point
    row_count_before_row = conn.execute("SELECT COUNT(*) FROM metrics_retention").fetchone()  # => a COUNT(*) query always returns exactly one row
    assert row_count_before_row is not None  # => confirms the COUNT(*) row genuinely came back
    row_count_before = row_count_before_row[0]  # => co-30: BOTH points present before the retention job runs
    assert row_count_before == 2  # => co-30: confirms both the old and recent point genuinely landed

    add_and_run_retention_policy(conn)  # => co-30: TSL tier (per this course's own license-awareness discipline, co-28) -- schedules AND immediately runs the drop

    remaining_rows = conn.execute("SELECT value FROM metrics_retention ORDER BY ts").fetchall()  # => co-30: what survived the retention job
    remaining_values = [row[0] for row in remaining_rows]  # => extracts the surviving values
    print(f"Rows before retention policy ran: {row_count_before}")  # => Output: Rows before retention policy ran: 2
    print(f"Rows after retention policy ran:  {len(remaining_values)}, values={remaining_values}")  # => Output: Rows after retention policy ran:  1, values=[2.0]
    assert remaining_values == [2.0]  # => co-30: ONLY the recent (1-hour-old) point survived -- the 40-day-old point's chunk was dropped
    print("The 40-day-old point (outside the 30-day retention window) was dropped; the 1-hour-old point (inside it) was retained")  # => Output line
    # => co-28: add_retention_policy is a TSL / Community feature (source-available, NOT OSI-approved) --
    # => distinct from the Apache-2.0-licensed create_hypertable/time_bucket API Examples 81-82 used
    conn.close()  # => always release what you open


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
