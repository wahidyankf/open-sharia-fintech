// Example 16: Shortest Path with shortestPath() (legacy but still supported).
// ONE query, two CREATE clauses with NO semicolon between them, so a and z stay bound
// across BOTH clauses -- this is what avoids accidentally creating a SECOND Ada/Zoe pair.
CREATE (a:Person {name: 'Ada'})-[:KNOWS]->(:Person {name: 'Bob'})-[:KNOWS]->(z:Person {name: 'Zoe'})
// => a 2-hop chain: Ada(a) -> Bob -> Zoe(z) -- a and z are ALIASED for reuse below
CREATE (a)-[:KNOWS]->(z);
// => a DIRECT 1-hop shortcut, reusing the SAME a and z -- not a second Ada/Zoe pair

MATCH (a:Person {name: 'Ada'}), (z:Person {name: 'Zoe'})
// => re-finds the ONE Ada and ONE Zoe node by their unique name property
MATCH p = shortestPath((a)-[:KNOWS*]-(z))
// => co-10: shortestPath() searches ALL paths between a and z, keeping only the shortest
RETURN length(p) AS hops;
// => co-10: shortestPath() finds the SHORTEST of all possible paths -- the direct 1-hop edge wins
