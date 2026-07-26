// Example 55: GDS: Project an In-Memory Graph. (co-26)
CREATE (:Person {name: 'Ada'})-[:KNOWS]->(:Person {name: 'Bob'})-[:KNOWS]->(:Person {name: 'Cid'});
// => 3 Person nodes, 2 KNOWS relationships -- the source graph GDS will project FROM

CALL gds.graph.project('social', 'Person', 'KNOWS')
// => 'social' is the PROJECTION's name -- every later gds.* call in this tier refers back to it
YIELD graphName, nodeCount, relationshipCount
// => the projection call itself reports back exactly what it just copied into memory
RETURN graphName, nodeCount, relationshipCount;
// => projects a NAMED in-memory graph "social" -- every gds.* call below refers back to this name
