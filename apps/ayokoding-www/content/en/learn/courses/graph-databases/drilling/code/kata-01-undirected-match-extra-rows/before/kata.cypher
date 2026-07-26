// Kata 1 (before): an undirected pattern matches a FOLLOWS edge from EITHER side,
// not just the direction the query actually needs.
CREATE (ada:Person {name: 'Ada'})-[:FOLLOWS]->(:Person {name: 'Bob'})
// => Ada FOLLOWS Bob -- this is the ONE person the report is supposed to surface
CREATE (:Person {name: 'Cid'})-[:FOLLOWS]->(ada);
// => Cid FOLLOWS Ada, the OPPOSITE direction -- Ada does NOT follow Cid back

// intent: list only the people ADA FOLLOWS.
MATCH (a:Person {name: 'Ada'})--(other:Person)
// BUG: no arrowhead -- this matches the FOLLOWS edge from EITHER endpoint's side
RETURN other.name
ORDER BY other.name;
