// Example 59: GDS: Node Similarity. (co-26, co-15)
CREATE (u1:User {name: 'Ada'})-[:BOUGHT]->(kb:Item {name: 'Keyboard'})
// => Ada's first purchase, kb aliased for reuse below
CREATE (u1)-[:BOUGHT]->(mon:Item {name: 'Monitor'})
// => Ada's second purchase -- her full purchased set is now {Keyboard, Monitor}, mon aliased for reuse
CREATE (u2:User {name: 'Bob'})-[:BOUGHT]->(kb)
// => Bob's first purchase -- the SAME Keyboard node as Ada's, not a namesake
CREATE (u2)-[:BOUGHT]->(mon)
// => Bob's second purchase -- the SAME Monitor node too, so his set matches Ada's EXACTLY
CREATE (u3:User {name: 'Cid'})-[:BOUGHT]->(:Item {name: 'Headset'});
// => Ada and Bob overlap on BOTH items; Cid overlaps with neither -- purposely maximal contrast

CALL gds.graph.project('purchases', ['User', 'Item'], 'BOUGHT');
// => a projection over TWO node labels (User, Item) linked by BOUGHT -- a bipartite projection

CALL gds.nodeSimilarity.stream('purchases')
// => streams one row per pair of users whose purchased-item sets overlap at all
YIELD node1, node2, similarity
// => node1/node2 are internal GDS handles -- gds.util.asNode() resolves them back to real nodes
RETURN gds.util.asNode(node1).name AS a, gds.util.asNode(node2).name AS b, similarity
// => resolves both handles back to real names
ORDER BY similarity DESC
// => sorted descending so the single highest-overlap pair surfaces first
LIMIT 1;  // => trims to just the single highest-similarity pair
// => Ada/Bob score similarity = 1.0 -- their purchased-item sets are IDENTICAL
