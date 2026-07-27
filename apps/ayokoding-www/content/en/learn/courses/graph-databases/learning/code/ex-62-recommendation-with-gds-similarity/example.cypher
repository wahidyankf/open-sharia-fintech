// Example 62: Recommendation Powered by GDS Similarity. (co-26, co-15)
CREATE (u1:User {name: 'Ada'})-[:BOUGHT]->(kb:Item {name: 'Keyboard'})
// => Ada's first purchase, kb aliased for reuse below
CREATE (u1)-[:BOUGHT]->(mon:Item {name: 'Monitor'})
// => Ada's second purchase -- Ada's set is {Keyboard, Monitor}, mon aliased for reuse below
CREATE (u2:User {name: 'Bob'})-[:BOUGHT]->(kb)
// => Bob's first purchase -- the SAME Keyboard node as Ada's, not a namesake
CREATE (u2)-[:BOUGHT]->(mon)
// => Bob's second purchase -- the SAME Monitor node too, so far identical to Example 59's fixture
CREATE (u2)-[:BOUGHT]->(:Item {name: 'Mousepad'});
// => same overlap shape as Example 59, PLUS Bob has one item (Mousepad) Ada does not

CALL gds.graph.project('purchases', ['User', 'Item'], 'BOUGHT');
// => a bipartite projection over User and Item, linked by BOUGHT

CALL gds.nodeSimilarity.stream('purchases')
// => streams one row per pair of users whose purchased-item sets overlap at all
YIELD node1, node2, similarity
// => node1/node2 are internal GDS handles -- resolved to real nodes on the next line
WITH gds.util.asNode(node1) AS a, gds.util.asNode(node2) AS b, similarity
// => WITH carries the resolved a/b/similarity forward into the filtering below
WHERE a.name = 'Ada' AND b:User
// => keeps only rows where Ada is one side, and the OTHER side is genuinely a User (not an Item)
ORDER BY similarity DESC
// => highest-similarity user first
LIMIT 1
// => keeps only Ada's single most-similar OTHER user -- Bob, on this fixture
MATCH (b)-[:BOUGHT]->(rec:Item)
// => everything the most-similar user (b) bought
WHERE NOT (a)-[:BOUGHT]->(rec)
// => excludes anything Ada already has -- the actual "new" recommendation candidate
RETURN rec.name;
// => Mousepad -- the top-similarity user's purchase Ada does not already have
