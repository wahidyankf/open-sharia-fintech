// Example 23: Bulk Load with LOAD CSV. (co-20)
LOAD CSV WITH HEADERS FROM 'file:///people.csv' AS row
MERGE (:Person {name: row.name});
// => WITH HEADERS exposes row.name via the CSV's first line -- MERGE keeps a rerun idempotent (co-06)

MATCH (p:Person) RETURN count(p) AS person_count;
// => equals the CSV's row count -- one node per data row, header line excluded
