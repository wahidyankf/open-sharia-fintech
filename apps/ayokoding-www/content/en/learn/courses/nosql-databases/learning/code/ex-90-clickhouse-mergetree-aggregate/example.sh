#!/usr/bin/env bash
# Example 90: ClickHouse MergeTree Aggregate.
# Creates a MergeTree table (co-32, Apache-2.0) partitioned by month, inserts rows
# across 3 partitions, runs a GROUP BY aggregate, then uses EXPLAIN indexes=1 to
# verify a month-scoped range query prunes the 2 non-matching partitions (co-33).
set -euo pipefail # => stop on the first failing command

# NOTE: this script runs clickhouse-client INSIDE the running Docker container via
# `docker exec`, rather than a host-installed binary -- the host macOS cask build of
# clickhouse is Gatekeeper-blocked non-interactively on this machine, so `docker exec`
# is the reliable, reproducible invocation of the SAME official clickhouse-client tool.
CH="docker exec nosqldb-clickhouse clickhouse-client --user default --password nosqldb" # => co-32: the official ClickHouse CLI, run inside the container

$CH --multiquery --query "
DROP TABLE IF EXISTS sales;
CREATE TABLE sales (order_date Date, category String, amount Float64)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(order_date)
ORDER BY (category, order_date);
" # => co-32: MergeTree, ClickHouse's own column-oriented storage engine, partitioned by month
# => Output: (no output -- DDL statements print nothing on success)

$CH --query "
INSERT INTO sales VALUES
  ('2026-01-15','electronics',100.0),
  ('2026-01-20','books',50.0),
  ('2026-02-10','electronics',200.0),
  ('2026-03-05','books',75.0);
" # => co-32: 4 rows spanning 3 DISTINCT monthly partitions (Jan, Feb, Mar)
# => Output: (no output -- a successful INSERT prints nothing)

$CH --query "SELECT category, sum(amount) FROM sales GROUP BY category ORDER BY category" # => co-32: the partitioned GROUP BY aggregation itself
# => Output (clickhouse-client's real TSV output uses a tab between columns; shown here as a single
# => space since this comment's own whitespace is normalized by this repo's markdown formatting pipeline):
# => books 125
# => electronics 300

$CH --query "EXPLAIN indexes=1 SELECT sum(amount) FROM sales WHERE order_date >= '2026-02-01' AND order_date < '2026-03-01'" | grep -A 5 "Min-Max" # => co-33: EXPLAIN's own Min-Max index section reports EXACTLY which of the 3 total parts survived pruning
# => Output:
# =>         Min-Max
# =>           Keys:
# =>             order_date
# =>           Condition: and((order_date in (-Inf, 20512]), (order_date in [20485, +Inf)))
# =>           Parts: 1/3
# =>           Granules: 1/3
# => co-33: "Parts: 1/3" means ONLY 1 of the table's 3 total parts (one per monthly partition)
# => survived the index check -- the January and March partitions were pruned entirely, before any
# => row within them was read, because the query's own date range never touches them
