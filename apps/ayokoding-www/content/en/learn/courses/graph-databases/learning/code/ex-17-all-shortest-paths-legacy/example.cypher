// Example 17: All Shortest Paths with allShortestPaths().
CREATE (a:Person {name: 'Ada'})-[:KNOWS]->(m1:Person {name: 'Mid1'})-[:KNOWS]->(z:Person {name: 'Zoe'})
// => first 2-hop route: Ada(a) -> Mid1 -> Zoe(z)
CREATE (a)-[:KNOWS]->(m2:Person {name: 'Mid2'})-[:KNOWS]->(z);
// => SECOND 2-hop route, same a and z reused -- TWO distinct paths now tie for shortest

MATCH (a:Person {name: 'Ada'}), (z:Person {name: 'Zoe'})
// => re-finds the one Ada and one Zoe node
MATCH p = allShortestPaths((a)-[:KNOWS*..4]-(z))
// => co-10: unlike shortestPath(), this returns EVERY tied-shortest path, not just one
RETURN length(p) AS hops, [n IN nodes(p) | n.name] AS via;
// => co-10: BOTH 2-hop paths come back -- neither is arbitrarily dropped for the other
