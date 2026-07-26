// Kata 1 (after): the arrowhead restores the ONE direction the report actually needs.
CREATE (ada:Person {name: 'Ada'})-[:FOLLOWS]->(:Person {name: 'Bob'})
CREATE (:Person {name: 'Cid'})-[:FOLLOWS]->(ada);

// THE FIX: -[:FOLLOWS]-> requires the SAME direction the data was created with.
MATCH (a:Person {name: 'Ada'})-[:FOLLOWS]->(other:Person)
RETURN other.name
ORDER BY other.name;
