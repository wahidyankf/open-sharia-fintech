-- Example 31: Recursive CTE Bill of Materials.
-- A bill-of-materials (BOM) explosion (co-03) answers "how many of each raw part
-- do I need to build ONE finished product?" -- quantities MULTIPLY down each level.
SET
  client_min_messages TO WARNING;

DROP TABLE IF EXISTS part CASCADE;

-- => resets state -- this example is fully self-contained
-- Same self-referencing adjacency-list shape as Example 7's org chart, but with
-- an extra qty_per_parent column -- the multiplier at each level, not just the
-- structural link.
CREATE TABLE part (
  id INTEGER PRIMARY KEY,
-- id is a plain integer identifier, unrelated to the multiplier math -- name is
-- what carries meaning in the final report below.
  name TEXT NOT NULL,
-- Just as in Example 7, the root's parent_id is NULL -- the recursion's anchor
-- is selected by WHERE id = 1, not by testing parent_id IS NULL, though either
-- approach would work for this single-root dataset.
  parent_id INTEGER REFERENCES part (id),
-- qty_per_parent means "how many of THIS part are needed to build ONE of its
-- immediate parent" -- a purely LOCAL ratio; the recursion's job is turning
-- these local ratios into a cumulative total from root to leaf.
  qty_per_parent INTEGER NOT NULL
);

-- => self-referencing FK, like Example 7's org chart
-- A 2-level bicycle: Wheel and Frame are direct children of Bicycle; Spoke and
-- Tire are children of Wheel -- deep enough to prove the multiplier COMPOUNDS
-- across levels (Spoke's 72 = 2 wheels x 36 spokes) rather than just copying down.
INSERT INTO
  part (id, name, parent_id, qty_per_parent)
VALUES
  (1, 'Bicycle', NULL, 1), -- => the root -- 1 bicycle is the top-level product
  (2, 'Wheel', 1, 2), -- => each bicycle needs 2 wheels
  (3, 'Frame', 1, 1), -- => each bicycle needs 1 frame
  (4, 'Spoke', 2, 36), -- => each WHEEL needs 36 spokes
  (5, 'Tire', 2, 1);

-- => each wheel needs 1 tire
-- Anchor: the root part, multiplier 1. Recursive term: multiply the CHILD's own
-- qty_per_parent by the PARENT's already-accumulated multiplier (co-03) -- this is
-- what makes spokes come out as 2 wheels x 36 spokes = 72, not just 36.
-- multiplier starts at 1 for the anchor (Bicycle needs exactly 1 of itself) --
-- every other part's multiplier is computed relative to that starting value.
WITH RECURSIVE
  bom AS (
    SELECT
      id,
      name,
      parent_id,
-- Same accumulator-column pattern as Example 7's depth column, but MULTIPLYING
-- instead of ADDING at each recursive step -- the recursion mechanics are
-- identical; only the arithmetic combining function changes.
      1 AS multiplier
    FROM
-- The anchor's FROM part with WHERE id = 1 scans the WHOLE part table looking
-- for one row -- fine at this tiny scale; a real BOM table would want an index
-- on id (already implicit, since id IS the primary key).
      part
    WHERE
      id = 1 -- => anchor: the Bicycle itself, multiplier 1
    UNION ALL
-- p.id, p.name, p.parent_id must again match the anchor's column list exactly
-- in count and type -- see Example 7's note on this same requirement.
    SELECT
      p.id,
      p.name,
      p.parent_id,
-- bom.multiplier * p.qty_per_parent is the entire algorithm: each level's
-- multiplier is the PARENT's multiplier scaled by how many of THIS part one
-- parent needs -- compounding naturally falls out of ordinary multiplication.
      bom.multiplier * p.qty_per_parent
    FROM
      part p
-- Joining CHILD parts to their already-processed PARENT row (not the other way
-- around) is what lets bom.multiplier already hold the fully-accumulated
-- multiplier from the root down to that parent before this level multiplies it further.
      JOIN bom ON p.parent_id = bom.id
      -- => recursive term: multiply DOWN the tree, not just add
  )
SELECT
  name,
  multiplier AS total_needed_per_bicycle
FROM
  bom
-- Excluding the root mirrors a real bill-of-materials report: nobody needs to
-- be told "you need 1 bicycle to build 1 bicycle" -- only the component list matters.
WHERE
  id != 1 -- => exclude the root -- we want components, not the product itself
-- Alphabetical ordering here is purely cosmetic -- it does not affect any of
-- the already-computed multiplier values.
ORDER BY
  name;

-- => Frame: 1, Spoke: 72 (2 wheels x 36), Tire: 2, Wheel: 2
-- This same multiply-down-the-tree pattern generalizes to any explosion
-- problem -- ingredient quantities in a recipe tree, dependency counts in a
-- build graph, or resource requirements in a project breakdown structure.
