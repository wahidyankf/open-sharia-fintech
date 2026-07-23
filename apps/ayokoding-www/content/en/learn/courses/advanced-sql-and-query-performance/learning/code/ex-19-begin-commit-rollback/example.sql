-- Example 19: BEGIN, COMMIT, and ROLLBACK.
-- BEGIN (co-11) opens a transaction: every write inside it is provisional until
-- COMMIT makes it durable, or ROLLBACK discards ALL of it -- both writes below, undone together.
SET
  client_min_messages TO WARNING;

DROP TABLE IF EXISTS account CASCADE;

-- => resets state -- this example is fully self-contained
-- balance uses NUMERIC(10, 2), the same money-safe precision pattern as price in
-- earlier examples -- transaction semantics here are independent of that choice,
-- but exact arithmetic still matters once real balances are being debited.
CREATE TABLE account (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  balance NUMERIC(10, 2) NOT NULL
);

-- => account table exists, currently empty
-- A single starting account keeps the before/after comparison trivial: one row,
-- one balance, easy to eyeball against the final SELECT's output.
INSERT INTO
  account (id, name, balance)
VALUES
  (1, 'checking', 500.00);

-- => one starting account, balance 500.00
-- BEGIN (co-11) starts the transaction -- both writes below are provisional.
-- Outside a BEGIN...COMMIT/ROLLBACK block, Postgres runs every statement in its
-- OWN implicit transaction, auto-committed immediately -- BEGIN is what turns
-- multiple statements into a SINGLE atomic unit that can still be undone.
BEGIN;

-- "balance = balance - 100" reads the CURRENT row's balance and writes back a
-- new value in one statement -- transactionally safe on its own, but this
-- example's point is what happens when a SECOND statement follows it.
UPDATE account
SET
  balance = balance - 100
WHERE
  id = 1;

-- => balance is now 400.00 -- but ONLY inside this transaction
-- This INSERT happens in the SAME transaction as the UPDATE above -- both are
-- still provisional together; nothing here has touched disk in a way any OTHER
-- connection could observe yet (see Example 27 for what other sessions see).
INSERT INTO
  account (id, name, balance)
VALUES
  (2, 'savings', 100.00);

-- => a second account appears -- also only provisional so far
-- ROLLBACK discards EVERY write since BEGIN, as if neither statement ever ran.
-- ROLLBACK has no way to undo "just the INSERT" or "just the UPDATE" --
-- transactions are all-or-nothing units; every write since the matching BEGIN
-- is discarded together, regardless of how many separate statements ran.
ROLLBACK;

-- Verify: the original balance is untouched and the savings account never persisted.
-- If COMMIT had been used instead of ROLLBACK, this SELECT would instead show
-- 2 rows (checking at 400.00, savings at 100.00) -- swap the keyword and re-run
-- to see the opposite outcome for yourself.
SELECT
  id,
  name,
  balance
FROM
  account
ORDER BY
  id;

-- => exactly 1 row: checking, balance still 500.00
