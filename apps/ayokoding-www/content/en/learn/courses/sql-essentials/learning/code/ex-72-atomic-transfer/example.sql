-- Example 72: Atomic Transfer.
CREATE TABLE account(id INTEGER PRIMARY KEY, name TEXT NOT NULL, balance REAL NOT NULL);
                                    -- => a tiny ledger -- 2 accounts, one debit/credit pair below
INSERT INTO account(id, name, balance) VALUES (1, 'checking', 100.0), (2, 'savings', 50.0);
                                    -- => starting balances -- the baseline for every check below

.headers on
.mode column
SELECT id, name, balance FROM account;
                                    -- => checking 100.0, savings 50.0 -- the starting state

-- A successful transfer: BOTH legs (debit + credit) succeed inside ONE transaction (co-18).
BEGIN;                              -- => opens the transaction -- neither leg is visible yet
UPDATE account SET balance = balance - 30.0 WHERE id = 1;
                                    -- => debit leg -- checking drops by 30
UPDATE account SET balance = balance + 30.0 WHERE id = 2;
                                    -- => credit leg -- savings gains the SAME 30
COMMIT;                            -- => both legs land together -- no half-transfer is EVER visible

SELECT id, name, balance FROM account;
                                    -- => checking 70.0, savings 80.0 -- 30 moved, nothing lost

-- A transfer we DELIBERATELY abandon after detecting a problem, before committing either leg.
BEGIN;                              -- => opens a SECOND, independent transaction
UPDATE account SET balance = balance - 1000.0 WHERE id = 1;
                                    -- => this debit would drive checking NEGATIVE -- a business rule
                                    -- => violation this application layer checks for itself
ROLLBACK;                          -- => undoes the just-issued debit -- nothing was ever persisted

SELECT id, name, balance FROM account;
                                    -- => STILL checking 70.0, savings 80.0 -- all-or-nothing held
