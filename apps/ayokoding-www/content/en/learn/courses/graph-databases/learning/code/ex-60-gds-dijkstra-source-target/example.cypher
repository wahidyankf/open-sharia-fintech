// Example 60: GDS: Dijkstra Source-Target. (co-26, co-10)
CREATE (a:Place {name: 'A'})-[:ROAD {cost: 10}]->(:Place {name: 'B'})-[:ROAD {cost: 10}]->(z:Place {name: 'Z'})
// => the LONGER route by weight: A->B->Z, total cost 10+10 = 20
CREATE (a)-[:ROAD {cost: 5}]->(:Place {name: 'C'})-[:ROAD {cost: 5}]->(z);
// => the SHORTER route by weight: A->C->Z, total cost 5+5 = 10 -- both routes are 2 hops
// long, so a hop-COUNTING shortest path could not tell them apart; only weighting distinguishes them

CALL gds.graph.project('roads', 'Place', 'ROAD', {relationshipProperties: 'cost'});
// => projects BOTH routes into memory, carrying the 'cost' property Dijkstra needs to weigh them

MATCH (a:Place {name: 'A'}), (z:Place {name: 'Z'})
// => binds the live source/target NODES that gds.shortestPath.dijkstra.stream needs as parameters
CALL gds.shortestPath.dijkstra.stream('roads', {
  sourceNode: a, targetNode: z, relationshipWeightProperty: 'cost'
  // => relationshipWeightProperty tells Dijkstra to minimize SUMMED cost, not hop count
})
YIELD totalCost
// => the WEIGHTED total of whichever route Dijkstra found cheapest
RETURN totalCost;
// => 10.0 -- the A->C->Z route, correctly chosen over the equal-HOP-length but heavier A->B->Z route
