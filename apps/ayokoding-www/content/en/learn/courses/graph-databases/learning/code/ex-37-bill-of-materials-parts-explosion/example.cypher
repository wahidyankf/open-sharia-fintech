// Example 37: Bill-of-Materials Parts Explosion. (co-14, co-09)
CREATE (bolt:Part {name: 'Bolt'})-[:PART_OF]->(bracket:Part {name: 'Bracket'})
      -[:PART_OF]->(frame:Part {name: 'Frame'})
// => Bolt is PART_OF Bracket; Bracket is PART_OF Frame -- a 2-hop assembly chain
CREATE (:Part {name: 'Screw'})-[:PART_OF]->(bracket);
// => a SECOND part feeding into the SAME bracket -- Bracket is made of Bolt AND Screw

MATCH (frame:Part {name: 'Frame'})<-[:PART_OF*]-(sub)
// => reversed *, unbounded -- every part in the WHOLE sub-assembly tree beneath Frame
RETURN sub.name;
// => hand-traced: Bracket (1 hop), Bolt (2 hops, via Bracket), Screw (2 hops, via Bracket)
