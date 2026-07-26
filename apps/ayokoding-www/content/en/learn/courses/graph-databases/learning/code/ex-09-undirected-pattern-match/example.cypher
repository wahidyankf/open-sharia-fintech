// Example 9: Undirected Pattern Match.
CREATE (:Person {name: 'Ada'})-[:KNOWS]->(:Person {name: 'Charles'});
// => created with a direction: Ada -> Charles, exactly like Example 3

// (a)--(b), no arrowhead (co-07), matches the edge from EITHER endpoint's perspective.
MATCH (a:Person)--(b:Person)
RETURN a.name, b.name;
// => TWO rows: (Ada, Charles) walked forward AND (Charles, Ada) walked backward -- same one edge (co-08)
