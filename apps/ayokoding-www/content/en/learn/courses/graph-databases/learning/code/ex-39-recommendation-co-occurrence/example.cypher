// Example 39: Recommendation by Co-Occurrence. (co-15, co-08)
CREATE (u:User {name: 'Ada'})-[:BOUGHT]->(shared:Item {name: 'Keyboard'})
// => Ada bought exactly one item, shared aliased for reuse below
CREATE (other:User {name: 'Bob'})-[:BOUGHT]->(shared)
// => Bob bought the SAME Keyboard node as Ada -- bound once and reused, not a second CREATE
// with a matching name, which would mint a structurally distinct node
CREATE (other)-[:BOUGHT]->(:Item {name: 'Mousepad'});
// => Ada and Bob BOTH bought Keyboard; Bob ALSO bought Mousepad -- Ada has not

MATCH (u:User {name: 'Ada'})-[:BOUGHT]->(:Item)<-[:BOUGHT]-(other)-[:BOUGHT]->(rec:Item)
// => 4-hop walk: Ada's item -> co-buyer -> co-buyer's OTHER purchase, bound as rec
WHERE NOT (u)-[:BOUGHT]->(rec)
// => the exclusion filter -- rec must NOT already be one of Ada's own purchases
RETURN rec.name, count(*) AS score
ORDER BY score DESC;
// => Mousepad recommended -- co-08 walks: shared item -> other buyer -> their OTHER purchase
