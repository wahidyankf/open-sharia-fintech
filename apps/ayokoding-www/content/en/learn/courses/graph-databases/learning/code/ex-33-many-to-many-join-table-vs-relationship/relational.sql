-- Example 33a: many-to-many via a JOIN TABLE.
-- => 3 tables total: 2 entity tables (student, course) + 1 junction table (enrollment)
CREATE TABLE student (id INTEGER PRIMARY KEY, name TEXT NOT NULL);

-- => the "one" entity side, no relationship info here
-- => id auto-increments via INTEGER PRIMARY KEY -- the same pattern every entity table below uses
CREATE TABLE course (id INTEGER PRIMARY KEY, name TEXT NOT NULL);

-- => the "other" entity side, also no relationship info
CREATE TABLE enrollment (
  student_id INTEGER NOT NULL,
  -- => foreign key by convention only -- SQLite does not enforce it without FOREIGN KEY syntax
  course_id INTEGER NOT NULL
  -- => paired with student_id, together forming the composite "who takes what" fact
);

-- => enrollment is the JOIN TABLE -- its only job is connecting the two entity tables
-- => it has no PRIMARY KEY of its own -- the pair (student_id, course_id) IS the only fact stored
-- => nothing here PREVENTS duplicate (student_id, course_id) rows without an added constraint
INSERT INTO
  student
VALUES
  (1, 'Ada');

-- => id 1, Ada -- becomes the JOIN anchor (student.id) resolved below
-- => nothing about "what Ada takes" lives on this row at all
INSERT INTO
  course
VALUES
  (1, 'Graph Theory');

-- => id 1, Graph Theory -- becomes the JOIN target (course.id) resolved below
-- => one student row, one course row -- neither knows about the other yet
INSERT INTO
  enrollment
VALUES
  (1, 1);

-- => (student_id 1, course_id 1) -- the ONLY row connecting Ada to Graph Theory
-- => a second course for Ada would be a SECOND row here, not a change to an existing one
-- => the fact "Ada takes Graph Theory" lives ONLY in this junction row
SELECT
  student.name,
  -- => projects the student side of the fact
  course.name
  -- => projects the course side of the fact -- both columns come from DIFFERENT tables
  -- => neither column comes from enrollment itself -- it only supplies the JOIN path
FROM
  student
  -- => the starting table -- everything else below joins outward from here
  JOIN enrollment ON enrollment.student_id = student.id
  -- => join 1: student to its enrollment rows
  -- => this is the ONLY point where student and enrollment connect at all
  JOIN course ON course.id = enrollment.course_id;

-- => join 2: enrollment row to the actual course
-- => TWO joins needed just to answer "who takes what"
-- => a THIRD student or course would still need only these SAME two joins to resolve
-- => contrast with Example 33b below -- the graph form needs ZERO extra joins for this same fact
