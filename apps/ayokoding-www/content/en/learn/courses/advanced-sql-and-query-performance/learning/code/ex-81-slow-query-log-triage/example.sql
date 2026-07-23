-- Example 81: Slow Query Log, Triage.
-- log_min_duration_statement (co-25) tells PostgreSQL to write ANY statement that
-- runs longer than a threshold to the server log, WITH its exact text and timing --
-- the standard first step for finding the query actually slowing down production.
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS daily_metric CASCADE;
                                    -- => resets state -- this example is fully self-contained
CREATE TABLE daily_metric(day_number INTEGER PRIMARY KEY, value NUMERIC(10,2) NOT NULL);
INSERT INTO daily_metric(day_number, value)
SELECT n, (100 + (n % 50))::NUMERIC FROM generate_series(1, 2500) AS n;

SET log_min_duration_statement = 100;
                                    -- => (co-25, co-26): log ONLY statements slower than 100ms --
                                    -- => set LOW enough to catch a real offender, high enough to
                                    -- => ignore routine fast queries and avoid flooding the log

-- A FAST query -- well under the 100ms threshold -- should NOT be logged.
SELECT COUNT(*) FROM daily_metric WHERE day_number < 10;

-- A SLOW query -- the O(n^2) self-join pattern from Example 67 -- genuinely
-- exceeds 100ms on this data and WILL be logged with its exact text + duration.
-- Wrapped in COUNT(*) so only ONE summary row prints -- the O(n^2) join cost
-- underneath is UNCHANGED; only the amount of output printed here is smaller.
SELECT COUNT(*) FROM (
    SELECT a.day_number, SUM(b.value) AS running_total
    FROM daily_metric a JOIN daily_metric b ON b.day_number <= a.day_number
    GROUP BY a.day_number
) AS slow_running_total;

RESET log_min_duration_statement;
                                    -- => turn logging back off -- this was a deliberate, scoped
                                    -- => diagnostic session, not a permanent production setting
