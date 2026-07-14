-- Example 57: Self Join
-- Run: sqlite3 app.db < example.sql

-- Dot-commands: print headers, align columns, spell out NULL instead of blank.
.headers on
.mode column
.nullvalue NULL

-- A self-join relates a table to ITSELF -- manager_id points back into the
-- SAME employee table, so every row can reference another row in that table.
CREATE TABLE employee (                        -- => a single table -- no separate manager table
  id INTEGER PRIMARY KEY,                     -- => aliases rowid, auto-assigned
  name TEXT NOT NULL,                         -- => employee's name, required
  manager_id INTEGER REFERENCES employee(id)  -- => FK to this SAME table's id
);

-- Ada has no manager (NULL) -- she's the top of the tree. Grace and Alan both
-- report to Ada; nobody reports to Grace or Alan.
INSERT INTO employee (id, name, manager_id) VALUES -- => 3 employees, 1 at the top
  (1, 'Ada Lovelace', NULL),                  -- => top of the tree -- no manager
  (2, 'Grace Hopper', 1),                     -- => reports to employee id 1 (Ada)
  (3, 'Alan Turing', 1);                      -- => reports to employee id 1 (Ada)

-- Join the table to a SECOND aliased copy of itself -- `e` for the employee
-- row, `m` for that same row's manager (also a row in employee). A plain JOIN
-- (not LEFT JOIN) drops Ada here since her manager_id is NULL -- no match in `m`.
SELECT e.name AS employee_name, m.name AS manager_name -- => two names, from the same table
FROM employee e                                 -- => `e` -- the employee's own row
JOIN employee m ON e.manager_id = m.id          -- => `m` is `e`'s manager row
ORDER BY e.id;                                  -- => deterministic row order
