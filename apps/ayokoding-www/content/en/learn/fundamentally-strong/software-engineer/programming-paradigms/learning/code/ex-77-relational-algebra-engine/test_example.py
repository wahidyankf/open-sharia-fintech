"""Example 77: pytest verification for Relational Algebra Engine."""

from example import Relation, join, project, select


def test_composed_query_matches_the_module_level_demo() -> None:
    employees: Relation = [
        {"emp_id": 1, "name": "alice", "dept_id": 10},
        {"emp_id": 2, "name": "bob", "dept_id": 20},
        {"emp_id": 3, "name": "carol", "dept_id": 10},
    ]
    departments: Relation = [{"dept_id": 10, "dept_name": "engineering"}, {"dept_id": 20, "dept_name": "sales"}]
    result = select(
        project(join(employees, departments, on="dept_id"), ["name", "dept_name"]),
        lambda row: row["dept_name"] == "engineering",
    )
    assert result == [
        {"name": "alice", "dept_name": "engineering"},
        {"name": "carol", "dept_name": "engineering"},
    ]


def test_join_with_no_matching_rows_returns_an_empty_relation() -> None:
    left: Relation = [{"id": 1, "x": "a"}]  # => no row here shares an id with `right`
    right: Relation = [{"id": 99, "y": "b"}]
    assert join(left, right, on="id") == []  # => an empty relation, not an error


# => Run: pytest -- Output: 2 passed
