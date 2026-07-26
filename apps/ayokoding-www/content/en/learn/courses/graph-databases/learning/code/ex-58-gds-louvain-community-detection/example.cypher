// Example 58: GDS: Louvain Community Detection. (co-26)
// Cluster 1: a fully-connected triangle.
CREATE (a1:Person {name: 'A1'})-[:KNOWS]->(a2:Person {name: 'A2'})-[:KNOWS]->(a3:Person {name: 'A3'})-[:KNOWS]->(a1);
// => 3 mutual edges, forming a closed triangle -- A1, A2, A3 form one dense cluster
// Cluster 2: a SEPARATE fully-connected triangle, with NO edges to cluster 1.
CREATE (b1:Person {name: 'B1'})-[:KNOWS]->(b2:Person {name: 'B2'})-[:KNOWS]->(b3:Person {name: 'B3'})-[:KNOWS]->(b1);
// => an IDENTICAL triangle shape, but with zero edges connecting it back to cluster 1

CALL gds.graph.project('social', 'Person', 'KNOWS');
// => projects both triangles into memory under the name 'social'

CALL gds.louvain.stream('social')
// => streams one row per node, each tagged with the community Louvain assigned it
YIELD nodeId, communityId
// => nodeId is an internal GDS handle -- gds.util.asNode() below resolves it back to a real node
RETURN gds.util.asNode(nodeId).name AS name, communityId  // => resolves the id back to the node's name
ORDER BY communityId, name;
// => A1/A2/A3 share ONE communityId; B1/B2/B3 share a DIFFERENT one -- 2 distinct clusters resolve
