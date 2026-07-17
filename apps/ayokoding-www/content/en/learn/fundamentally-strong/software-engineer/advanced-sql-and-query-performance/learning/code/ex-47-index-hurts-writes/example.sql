-- Example 47: Index Hurts Writes.
-- Every index (co-22) is a SEPARATE structure the engine must update on every
-- INSERT -- more indexes means more write work per row, even though NONE of that
-- work is visible in the INSERT statement's own syntax.
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS few_indexes, many_indexes CASCADE;
                                    -- => resets state -- this example is fully self-contained
-- Identical column shapes on both tables -- only the NUMBER of indexes differs,
-- isolating index count as the one variable this benchmark measures.
CREATE TABLE few_indexes(id INTEGER PRIMARY KEY, a INTEGER, b INTEGER, c INTEGER, d INTEGER);
                                    -- => only the PRIMARY KEY's own index -- 1 index total
CREATE TABLE many_indexes(id INTEGER PRIMARY KEY, a INTEGER, b INTEGER, c INTEGER, d INTEGER);
-- Four single-column B-tree indexes, one per non-key column -- each one is
-- ordinary and individually reasonable; the cost being measured is their SUM.
CREATE INDEX idx_many_a ON many_indexes(a);
CREATE INDEX idx_many_b ON many_indexes(b);
CREATE INDEX idx_many_c ON many_indexes(c);
CREATE INDEX idx_many_d ON many_indexes(d);
                                    -- => PRIMARY KEY + 4 more indexes -- 5 indexes total, SAME row shape

\timing on
                                    -- => measure both inserts under identical conditions
-- Identical row COUNT, identical VALUES generator -- \timing measures wall-clock
-- duration for the INSERT itself, index maintenance included.
INSERT INTO few_indexes(id, a, b, c, d)
SELECT n, n % 100, n % 200, n % 300, n % 400 FROM generate_series(1, 200000) AS n;
                                    -- => 200,000 rows into the 1-index table

INSERT INTO many_indexes(id, a, b, c, d)
SELECT n, n % 100, n % 200, n % 300, n % 400 FROM generate_series(1, 200000) AS n;
                                    -- => the SAME 200,000 rows into the 5-index table
\timing off
