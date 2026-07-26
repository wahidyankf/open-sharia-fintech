// Example 39: Recommendation by Co-Occurrence. (co-15, co-08)
CREATE (u:User {name: 'Ada'})-[:BOUGHT]->(:Item {name: 'Keyboard'})
// => Ada bought exactly one item
CREATE (other:User {name: 'Bob'})-[:BOUGHT]->(:Item {name: 'Keyboard'})
// => Bob bought the SAME item as Ada -- the shared signal the pattern below finds
CREATE (other)-[:BOUGHT]->(:Item {name: 'Mousepad'});
// => Ada and Bob BOTH bought Keyboard; Bob ALSO bought Mousepad -- Ada has not

MATCH (u:User {name: 'Ada'})-[:BOUGHT]->(:Item)<-[:BOUGHT]-(other)-[:BOUGHT]->(rec:Item)
// => 4-hop walk: Ada's item -> co-buyer -> co-buyer's OTHER purchase, bound as rec
WHERE NOT (u)-[:BOUGHT]->(rec)
// => the exclusion filter -- rec must NOT already be one of Ada's own purchases
RETURN rec.name, count(*) AS score
ORDER BY score DESC;
// => Mousepad recommended -- co-08 walks: shared item -> other buyer -> their OTHER purchase
