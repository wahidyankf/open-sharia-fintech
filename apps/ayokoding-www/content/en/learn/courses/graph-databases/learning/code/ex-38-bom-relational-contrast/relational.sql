-- Example 38a: the SAME bill-of-materials explosion, a recursive CTE (co-14).
-- one table for every part, self-referencing to express the assembly hierarchy
CREATE TABLE part (
  id INTEGER PRIMARY KEY,
  -- => auto-incrementing identity -- the same PRIMARY KEY pattern every table in this course uses
  name TEXT NOT NULL,
  -- => the human-readable label the final SELECT below eventually returns
  part_of INTEGER
  -- => nullable, self-referencing -- NULL means "top of the assembly, part of nothing"
);

-- => part_of is a self-referencing foreign key -- the SQL analogue of :PART_OF
-- => one row per part -- the whole hierarchy lives entirely in this single self-referencing column
-- => 4 parts, 3 assembly levels deep: Frame -> Bracket -> {Bolt, Screw}
INSERT INTO
  part
VALUES
  (1, 'Frame', NULL),
  -- => the TOP assembly -- part_of NULL means "not part of anything else"
  (2, 'Bracket', 1),
  -- => part_of 1 means "Bracket is part of Frame" -- the base case's target below
  (3, 'Bolt', 2),
  -- => part_of 2 means "Bolt is part of Bracket"
  (4, 'Screw', 2);

-- => part_of 2 again -- Bracket has TWO children, Bolt and Screw, both pointing back to id 2
-- => Frame itself never appears as a part_of value -- nothing claims to be "part of Frame's parent"
-- => a second child of Bracket -- Bracket is made of BOTH Bolt and Screw
-- the recursive CTE itself -- base case, then a repeated recursive case, unioned together
-- => "recursive" here means SQLite re-runs the SELECT after UNION ALL until it adds zero new rows
WITH RECURSIVE
  -- => RECURSIVE is required here -- a plain WITH would reject the self-reference in the JOIN below
  sub_parts (id, name) AS (
    -- => sub_parts is the CTE's own name -- the recursive half below refers back to it by name
    -- => declares the CTE's shape up front -- two columns, id and name, matching both SELECTs below
    SELECT
      id,
      -- => seeds the id column of sub_parts
      name
      -- => seeds the name column of sub_parts
    FROM
      part
      -- => the base case reads directly from the raw part table, not from sub_parts itself
    WHERE
      part_of = 1 -- base case: direct children of Frame
      -- => runs EXACTLY ONCE -- seeds sub_parts with Bracket's direct children, id 2 only
    UNION ALL
    -- => UNION ALL is what keeps FEEDING the recursion its own prior output
    -- => UNION (no ALL) would also de-duplicate rows -- unnecessary here since ids are already unique
    SELECT
      p.id,
      -- => the recursive half's id column, unioned onto the base case's rows
      p.name
      -- => the recursive half's name column
    FROM
      part p
      -- => aliased p -- every part row is a CANDIDATE child this round, filtered by the JOIN below
      JOIN sub_parts sp ON p.part_of = sp.id -- recursive case: children of children
      -- => re-runs each round against whatever sub_parts already holds, growing it by one level
      -- => round 1 matches Bolt and Screw (part_of 2); round 2 finds no new matches and stops
  )
  -- => the recursion terminates when a round finds no new matching rows
SELECT
  name
  -- => projects only the name column from the fully-expanded sub_parts result
FROM
  sub_parts;

-- => sub_parts now holds every descendant -- base case rows PLUS every recursive round's rows
-- => output: Bracket, Bolt, Screw -- Frame itself is excluded, WHERE seeded ONLY at part_of = 1
-- => the recursive UNION ALL must be written explicitly, base case + recursive case, by hand
-- => forgetting the recursive JOIN condition risks an infinite loop -- Cypher's * has no such risk
-- => a 5th assembly level would need ZERO query changes -- the recursion already handles any depth
