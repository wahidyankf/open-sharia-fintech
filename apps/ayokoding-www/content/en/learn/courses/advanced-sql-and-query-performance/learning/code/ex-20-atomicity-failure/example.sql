-- Example 20: Atomicity Failure.
-- PostgreSQL's atomicity guarantee (co-11) is strict: the MOMENT one statement in a
-- transaction errors, the whole transaction is marked "aborted" -- every later
-- statement is rejected too, even valid ones, until you ROLLBACK.
SET
  client_min_messages TO WARNING;

DROP TABLE IF EXISTS account CASCADE;

-- => resets state -- this example is fully self-contained
-- CHECK (balance >= 0) is a table-level integrity rule enforced by Postgres
-- itself on every INSERT/UPDATE -- unlike the application-level validation that
-- would need to run BEFORE issuing a write, this check cannot be bypassed.
CREATE TABLE account (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  balance NUMERIC(10, 2) NOT NULL CHECK (balance >= 0)
);

-- => CHECK enforces balance can never go negative
-- One starting account at 500.00 -- comfortably enough for the 'savings' insert
-- below to succeed, but not enough to survive the 1000.00 debit that follows it.
INSERT INTO
  account (id, name, balance)
VALUES
  (1, 'checking', 500.00);

-- => one starting account, balance 500.00
-- No explicit comment repeated here for BEGIN itself -- see Example 19 for what
-- BEGIN does; this example's focus is what happens when a LATER statement fails.
BEGIN;

-- This INSERT is individually valid and succeeds -- the point of this example is
-- that its validity alone will NOT be enough to save it once a later statement
-- in the same transaction fails.
INSERT INTO
  account (id, name, balance)
VALUES
  (2, 'savings', 100.00);

-- => succeeds so far -- this write is still provisional
-- Subtracting 1000 from 500 is arithmetically fine -- CHECK constraints run at
-- WRITE time, evaluating the RESULTING row, not the arithmetic expression itself;
-- -500 fails balance >= 0 the instant Postgres tries to store that new row.
UPDATE account
SET
  balance = balance - 1000
WHERE
  id = 1;

-- => 500 - 1000 = -500 violates CHECK(balance >= 0)
-- => raises: new row for relation "account" violates check constraint
-- => the transaction is now ABORTED -- every command below fails too
-- This statement is syntactically and semantically perfect on its own -- it
-- fails ONLY because the transaction is already marked aborted from the CHECK
-- violation above; Postgres will not even attempt to validate/execute it.
INSERT INTO
  account (id, name, balance)
VALUES
  (3, 'reserve', 50.00);

-- => rejected even though it is perfectly valid on its own
-- => raises: current transaction is aborted, commands ignored
-- Postgres offers no "resume" from an aborted transaction -- unlike a savepoint-
-- scoped failure (which can ROLLBACK TO SAVEPOINT and continue), a bare aborted
-- transaction can only be fully rolled back, never partially recovered.
ROLLBACK;

-- => the only way out of an aborted transaction is ROLLBACK
-- Verify: NEITHER the valid 'savings' insert NOR the failed UPDATE survived --
-- atomicity means "all or nothing," and here it was "nothing."
-- Note that even the 'savings' INSERT -- which never violated anything -- is
-- gone too: atomicity does not distinguish between the statement that caused
-- the failure and innocent statements that merely shared its transaction.
SELECT
  id,
  name,
  balance
FROM
  account
ORDER BY
  id;

-- => exactly 1 row: checking, balance still 500.00
