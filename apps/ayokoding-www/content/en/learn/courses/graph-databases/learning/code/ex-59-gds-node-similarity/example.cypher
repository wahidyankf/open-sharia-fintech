// Example 59: GDS: Node Similarity. (co-26, co-15)
CREATE (u1:User {name: 'Ada'})-[:BOUGHT]->(:Item {name: 'Keyboard'})
// => Ada's first purchase
CREATE (u1)-[:BOUGHT]->(:Item {name: 'Monitor'})
// => Ada's second purchase -- her full purchased set is now {Keyboard, Monitor}
CREATE (u2:User {name: 'Bob'})-[:BOUGHT]->(:Item {name: 'Keyboard'})
// => Bob's first purchase -- overlaps with Ada's Keyboard
CREATE (u2)-[:BOUGHT]->(:Item {name: 'Monitor'})
// => Bob's second purchase -- his set {Keyboard, Monitor} matches Ada's EXACTLY
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
