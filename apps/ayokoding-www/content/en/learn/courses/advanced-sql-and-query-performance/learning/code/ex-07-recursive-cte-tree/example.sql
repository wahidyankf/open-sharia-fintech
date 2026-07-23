-- Example 7: Recursive CTE Tree.
-- The same anchor + recursive-term shape from Example 6 (co-03) walks a real
-- self-referencing hierarchy here: every employee points at their manager_id.
-- Suppress routine NOTICE messages (e.g. table-does-not-exist-yet on a
-- fresh database) so output below stays focused on the query results.
SET
  client_min_messages TO WARNING;

DROP TABLE IF EXISTS employee CASCADE;

-- => resets state -- this example is fully self-contained
-- A self-referencing foreign key (manager_id -> employee.id) is the classic
-- "adjacency list" way to store a tree/hierarchy in one table -- Examples 30
-- and 31 apply this exact recursive-CTE pattern to a cyclic graph and a
-- multi-level bill-of-materials, respectively.
CREATE TABLE employee (
  id INTEGER PRIMARY KEY,
-- name is NOT NULL (every employee must have a display name) while manager_id
-- is nullable -- NULL is the only way to represent "has no manager" for the root.
  name TEXT NOT NULL,
-- REFERENCES employee(id) pointing at the table's OWN primary key is legal --
-- Postgres has no special-case restriction on self-referencing foreign keys;
-- the default ON DELETE RESTRICT still applies (a manager cannot be deleted
-- while a report still references them).
  manager_id INTEGER REFERENCES employee (id)
);

-- => self-referencing FK: manager_id points at another employee.id
-- Grace's row uses NULL for manager_id to mark her as the root -- WHERE
-- manager_id IS NULL would be a more GENERIC anchor predicate than the
-- hardcoded "id = 1" used below; either works for this single-root dataset.
INSERT INTO
  employee (id, name, manager_id)
VALUES
  (1, 'Grace (CTO)', NULL), -- => the root -- no manager, NULL stops the chain upward
  (2, 'Ada (VP Eng)', 1), -- => reports to Grace
  (3, 'Alan (VP Data)', 1), -- => also reports to Grace
  (4, 'Linus (Eng Lead)', 2), -- => reports to Ada -- two levels below Grace
  (5, 'Barbara (Eng)', 4);

-- => reports to Linus -- three levels below Grace
-- Anchor: the ONE row we start from (Grace, id=1). Recursive term: JOIN employee
-- back to org_tree ON manager_id = org_tree.id, walking one level down each pass.
-- depth is an ACCUMULATOR column: the anchor seeds it at 0, and each recursive
-- pass adds 1 -- this running-counter pattern generalizes to any recursive CTE
-- that needs to track "how many hops so far" (path length, level, generation),
-- not just this specific org-chart walk.
WITH RECURSIVE
  org_tree AS (
    SELECT
      id,
      name,
      manager_id,
-- 0 AS depth is a LITERAL, not a column reference -- Postgres infers its type
-- (integer) from context and matches it against depth's type in the recursive
-- term (org_tree.depth + 1), which must be assignable to the same column type.
      0 AS depth
    FROM
      employee
    WHERE
      id = 1 -- => anchor: start at Grace, depth 0
    UNION ALL
-- The recursive term's SELECT list must match the anchor's in column COUNT
-- and compatible TYPES, in the same order -- swapping e.name and e.id here
-- would still run, but would silently mislabel every row from the second
-- pass onward, since positions (not names) determine the output column.
    SELECT
      e.id,
      e.name,
      e.manager_id,
      org_tree.depth + 1
    FROM
-- Joining employee e back to org_tree ON e.manager_id = org_tree.id grows the
-- tree outward one generation per pass -- this works ONLY because the data is
-- guaranteed acyclic by the application; the table schema itself does not
-- prevent a manager_id cycle, which is exactly what Example 30 explores.
      employee e
      JOIN org_tree ON e.manager_id = org_tree.id
      -- => recursive term: finds employees whose manager
      -- => was just added, one depth level deeper each pass
  )
SELECT
  name,
  depth
FROM
  org_tree
-- Recursive CTEs make no guarantee about the ORDER rows are produced in --
-- relying on insertion/recursion order for display would be fragile; the
-- explicit ORDER BY here is what actually guarantees depth-then-name ordering.
ORDER BY
  depth,
  name;

-- => all 5 rows: Grace herself plus every descendant
-- Cost-wise, this recursive CTE re-runs the JOIN once per depth level -- fine
-- for a handful of org levels, but Example 65's shortest-path walk shows where
-- that repeated-join cost starts to matter at larger graph sizes.
