// Kata 4 (before): an unbounded * traverses as far as the graph goes, not just
// the "nearby" 2-hop neighborhood the widget is actually supposed to show.
CREATE (:Person {name: 'Ada'})-[:KNOWS]->(:Person {name: 'Bob'})
      -[:KNOWS]->(:Person {name: 'Cid'})-[:KNOWS]->(:Person {name: 'Dee'})
      -[:KNOWS]->(:Person {name: 'Eve'});
// => a 4-hop chain: Ada -> Bob -> Cid -> Dee -> Eve

// intent: show Ada's NEARBY network, within 2 hops.
MATCH (a:Person {name: 'Ada'})-[:KNOWS*]->(b:Person)
// BUG: unbounded * has no upper limit -- it walks the WHOLE connected chain, not just 2 hops
RETURN b.name
ORDER BY b.name;
