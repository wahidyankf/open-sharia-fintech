// Example 11: MERGE with ON CREATE / ON MATCH.
// First run: the node does not exist -> the ON CREATE branch fires (co-06).
MERGE (p:Person {name: 'Ada'})
// => no matching node exists yet -- this MERGE call CREATES it
ON CREATE SET p.firstSeen = 1
// => fires because this run just created p
ON MATCH SET p.seen = coalesce(p.seen, 0) + 1;
// => does NOT fire this run -- p.firstSeen = 1 is set; p.seen stays untouched

// Second run: the SAME pattern now exists -> the ON MATCH branch fires instead.
MERGE (p:Person {name: 'Ada'})
// => a node with this exact pattern NOW exists -- this MERGE call MATCHES it instead
ON CREATE SET p.firstSeen = 1
// => does NOT re-fire -- p already existed before this second run started
ON MATCH SET p.seen = coalesce(p.seen, 0) + 1;
// => fires instead -- p.firstSeen stays 1; p.seen becomes 1 (coalesce(null,0)+1)

MATCH (p:Person {name: 'Ada'})
// => re-reads the single node after both MERGE runs above
RETURN p.firstSeen, p.seen;
// => confirms firstSeen=1 (set once) and seen=1 (incremented once, on the second run only)
