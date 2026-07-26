// Example 1: Create a Single Node.
// CREATE (co-06) unconditionally writes the pattern -- run this twice and you get TWO nodes,
// unlike MERGE (Example 10), which would only ever leave you with one.
CREATE (:Person {name: 'Ada', born: 1815});
// => one new node, labeled :Person (co-01), with two properties: name and born
// => properties are typed values (string, integer here) -- not columns in a fixed schema

// MATCH + WHERE (co-05, previewed here) confirms exactly one row comes back.
MATCH (p:Person {name: 'Ada'})
RETURN p;
// => returns exactly one row: the node just created, echoed back with all its properties
