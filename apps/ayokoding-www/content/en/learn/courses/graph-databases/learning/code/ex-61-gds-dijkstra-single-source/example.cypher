// Example 61: GDS: Dijkstra Single-Source. (co-26, co-10)
CREATE (a:Place {name: 'A'})-[:ROAD {cost: 5}]->(:Place {name: 'B'})-[:ROAD {cost: 5}]->(:Place {name: 'C'});
// => a straight chain: A -(5)-> B -(5)-> C -- distances from A: B=5, C=10

CALL gds.graph.project('roads', 'Place', 'ROAD', {relationshipProperties: 'cost'});
// => projects the chain into memory, carrying the 'cost' property this algorithm needs

MATCH (a:Place {name: 'A'})
// => binds the live source NODE -- the single starting point for every distance computed below
CALL gds.allShortestPaths.dijkstra.stream('roads', {
  // => single-source variant: no targetNode this time
  sourceNode: a, relationshipWeightProperty: 'cost'
})  // => end of the single-source Dijkstra call
YIELD targetNode, totalCost
// => one row per reachable node, each with its own weighted distance from the source
RETURN gds.util.asNode(targetNode).name AS target, totalCost  // => resolves the handle to a name
ORDER BY totalCost;
// => B=5.0, C=10.0 -- matching each individually-computed shortest distance from A
