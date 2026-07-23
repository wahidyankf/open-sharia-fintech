-- Capstone: report.sql -- a window-function + recursive-CTE report in ONE query.
-- org_depth (co-03) walks the manager_id chain seed.sql just loaded; the outer SELECT's
-- RANK() and SUM() OVER (co-04, co-05) rank and running-total each department's salaries
-- without collapsing any of the 18 employee rows -- exactly the shape GROUP BY cannot
-- produce on its own.
WITH RECURSIVE org_depth AS (
  SELECT
    id,
    name,
    manager_id,
    department_id,
    salary,
    0 AS depth
  FROM
    employee
  WHERE
    manager_id IS NULL -- => anchor: the ONE row with no manager -- Grace, the CEO
  UNION ALL
  SELECT
    e.id,
    e.name,
    e.manager_id,
    e.department_id,
    e.salary,
    od.depth + 1
  FROM
    employee e
    JOIN org_depth od ON e.manager_id = od.id
    -- => recursive term: every employee whose manager was just added, one level deeper
)
SELECT
  d.name AS department,
  od.name AS employee,
  od.depth,
  od.salary,
  RANK() OVER (
    PARTITION BY
      od.department_id
    ORDER BY
      od.salary DESC
  ) AS dept_salary_rank,
  -- => co-06 -- 1 = highest-paid in THIS department, ties share a rank
  SUM(od.salary) OVER (
    PARTITION BY
      od.department_id
    ORDER BY
      od.salary DESC ROWS BETWEEN UNBOUNDED PRECEDING
      AND CURRENT ROW
  ) AS dept_cumulative_salary
  -- => co-04, co-05 -- running total of THIS department's salaries, highest-paid first
FROM
  org_depth od
  JOIN department d ON d.id = od.department_id
ORDER BY
  department,
  dept_salary_rank;
