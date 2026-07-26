// Example 40: Recommendation with a Minimum-Overlap Threshold. (co-15, co-23)
CREATE (u:User {name: 'Ada'})-[:BOUGHT]->(:Item {name: 'Keyboard'})
// => Ada's first item, u aliased for reuse
CREATE (u)-[:BOUGHT]->(:Item {name: 'Monitor'})
// => Ada's second item
CREATE (strong:User {name: 'Bob'})-[:BOUGHT]->(:Item {name: 'Keyboard'})
// => Bob shares item #1 with Ada
CREATE (strong)-[:BOUGHT]->(:Item {name: 'Monitor'})
// => Bob shares item #2 with Ada too -- overlap = 2
CREATE (strong)-[:BOUGHT]->(:Item {name: 'Mousepad'})
// => Bob's OWN extra item, the eventual recommendation candidate
CREATE (weak:User {name: 'Cid'})-[:BOUGHT]->(:Item {name: 'Keyboard'})
// => Cid shares only ONE item with Ada -- overlap = 1
CREATE (weak)-[:BOUGHT]->(:Item {name: 'Headset'});
// => Bob shares 2 items with Ada (strong overlap); Cid shares only 1 (weak overlap)

MATCH (u:User {name: 'Ada'})-[:BOUGHT]->(shared:Item)<-[:BOUGHT]-(other)
// => matches every (shared item, co-buyer) pair for Ada
// co-23: WITH computes a per-other-user overlap COUNT before the recommendation stage runs
WITH u, other, count(DISTINCT shared) AS overlap
// => aggregates PER co-buyer -- overlap is now a count, not individual shared-item rows
WHERE overlap >= 2
// => the threshold gate -- only co-buyers meeting this bar reach the next MATCH
MATCH (other)-[:BOUGHT]->(rec:Item)
// => the surviving co-buyer's OWN full purchase list
WHERE NOT (u)-[:BOUGHT]->(rec)
// => excludes anything Ada already owns
RETURN DISTINCT rec.name;
// => co-15: only Bob (overlap=2) contributes -- Cid's single shared item never clears the bar
