// Example 56: GDS: PageRank. (co-26)
CREATE (hub:Person {name: 'Hub'})
// => the single node every other person in this fixture points AT
CREATE (hub)<-[:KNOWS]-(:Person {name: 'A'})
// => A -> Hub, one of three inbound edges this fixture plants
CREATE (hub)<-[:KNOWS]-(:Person {name: 'B'})
// => B -> Hub, the second inbound edge
CREATE (hub)<-[:KNOWS]-(:Person {name: 'C'});
// => C -> Hub, the third inbound edge -- Hub is pointed AT by 3 different people

CALL gds.graph.project('social', 'Person', 'KNOWS');
// => projects the fixture above into memory under the name 'social'

CALL gds.pageRank.stream('social')
// => streams one row per node, scored by the whole graph's link structure
YIELD nodeId, score
// => nodeId is an internal GDS handle -- gds.util.asNode() below resolves it back to a real node
RETURN gds.util.asNode(nodeId).name AS name, score  // => resolves the id back to a real node's name
ORDER BY score DESC;
// => Hub scores HIGHEST -- it is the target of the most incoming KNOWS edges in this fixture
