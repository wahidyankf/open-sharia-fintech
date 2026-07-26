// Example 57: GDS: Betweenness Centrality. (co-26)
CREATE (a1:Person {name: 'A1'})-[:KNOWS]->(a2:Person {name: 'A2'})
// => the "A" side: a small 2-node chain
CREATE (bridge:Person {name: 'Bridge'})
// => a single node that will connect BOTH sides -- the only crossing point
CREATE (a1)-[:KNOWS]->(bridge)-[:KNOWS]->(b1:Person {name: 'B1'})-[:KNOWS]->(:Person {name: 'B2'});
// => Bridge is the ONLY connection between the "A" side and the "B" side of this graph

CALL gds.graph.project('social', 'Person', 'KNOWS');
// => projects the fixture above into memory under the name 'social'

CALL gds.betweenness.stream('social')
// => streams one row per node, scored by how often it sits on a shortest path
YIELD nodeId, score
// => nodeId is an internal GDS handle -- gds.util.asNode() below resolves it back to a real node
RETURN gds.util.asNode(nodeId).name AS name, score  // => resolves the id back to a real node's name
// => ordering is not required for LIMIT 1 to work, but makes the highest score explicit
ORDER BY score DESC
LIMIT 1;
// => Bridge scores HIGHEST -- every A-to-B shortest path is forced to pass through it
