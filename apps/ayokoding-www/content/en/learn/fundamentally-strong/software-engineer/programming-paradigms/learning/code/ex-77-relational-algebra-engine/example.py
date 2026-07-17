"""Example 77: Relational Algebra Engine."""

from collections.abc import Callable  # => types the SELECT predicate below

Row = dict[str, object]  # => one relation "row" as a plain dict
Relation = list[Row]  # => a relation is just a list of rows -- no database needed


def select(relation: Relation, predicate: Callable[[Row], bool]) -> Relation:  # => relational SELECT (sigma): filter rows
    return [row for row in relation if predicate(row)]  # => "the rows satisfying this condition"


def project(relation: Relation, columns: list[str]) -> Relation:  # => relational PROJECT (pi): pick columns
    return [{col: row[col] for col in columns} for row in relation]  # => "just these fields, from every row"


def join(left: Relation, right: Relation, on: str) -> Relation:  # => relational JOIN: combine matching rows
    result: Relation = []  # => accumulates every matching pair of rows
    for lrow in left:  # => the engine's own join algorithm -- callers never see this loop
        for rrow in right:  # => nested loop: every left row checked against every right row
            if lrow[on] == rrow[on]:  # => the join predicate: matching values in the `on` column
                result.append({**lrow, **rrow})  # => merge both rows' fields into one combined row
    return result  # => every matching row-pair, merged


employees: Relation = [  # => a small in-memory "table"
    {"emp_id": 1, "name": "alice", "dept_id": 10},  # => dept 10
    {"emp_id": 2, "name": "bob", "dept_id": 20},  # => dept 20
    {"emp_id": 3, "name": "carol", "dept_id": 10},  # => dept 10, same as alice
]  # => closes the employees relation
departments: Relation = [  # => a second small in-memory "table"
    {"dept_id": 10, "dept_name": "engineering"},  # => matches alice and carol on dept_id
    {"dept_id": 20, "dept_name": "sales"},  # => matches bob on dept_id
]  # => closes the departments relation

# => a COMPOSED query: join employees to departments, then project just name and dept_name, then
# => select only engineering -- three relational operators chained together, no explicit loop written here
composed_result = select(  # => outermost operator: filters the projected join result
    project(join(employees, departments, on="dept_id"), ["name", "dept_name"]),  # => join, then project
    lambda row: row["dept_name"] == "engineering",  # => the select predicate
)  # => closes the composed query -- three operators, zero explicit loops at the call site
print(composed_result)  # => alice and carol are both in engineering; bob is filtered out (sales)
# => Output: [{'name': 'alice', 'dept_name': 'engineering'}, {'name': 'carol', 'dept_name': 'engineering'}]
