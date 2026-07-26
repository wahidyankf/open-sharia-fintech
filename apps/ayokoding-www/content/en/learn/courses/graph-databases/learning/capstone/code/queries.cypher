// Capstone Step 2: Neighborhood and Friends-of-Friends Queries. (co-05, co-08, co-09)
// Both queries assume load.py has already run against the same Neo4j instance.

// Query 1 -- neighborhood: who else bought anything Ada bought?
MATCH (u:Person {name: 'Ada'})-[:BOUGHT]->(i:Item)<-[:BOUGHT]-(other:Person)  // => Query 1
// => a 2-hop pattern -- Ada's own purchase, then back OUT to any other buyer of the same item
RETURN DISTINCT other.name AS name;
// => co-08: DISTINCT avoids one duplicate row per shared item, if there were more than one

// Query 2 -- friends-of-friends: everyone reachable from Ada within 2 KNOWS hops.
MATCH (a:Person {name: 'Ada'})-[:KNOWS*1..2]-(b:Person)
// => co-09: *1..2 bounds the traversal -- direct friends AND friends-of-friends, nothing further
RETURN DISTINCT b.name AS name ORDER BY name;
// => sorted for a deterministic, checkable order
