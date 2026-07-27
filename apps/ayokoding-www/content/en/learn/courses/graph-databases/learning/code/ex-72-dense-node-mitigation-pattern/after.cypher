// Example 72b: AFTER -- accounts are bucketed through intermediate GROUP nodes first. (co-17, co-11)
CREATE CONSTRAINT verified_group_bucket FOR (g:VerifiedGroup) REQUIRE g.bucket IS UNIQUE;
// => co-22: without this, the MERGE below falls back to a full label scan on every write instead
// of an indexed unique-node lookup -- see Example 20 for the same constraint-before-MERGE pattern

UNWIND range(1, 5) AS i
// => the SAME 5 accounts as the "before" form, for a direct comparison
MERGE (g:VerifiedGroup {bucket: i % 4})
// => a FIXED bucket COUNT (4 via modulo), NOT a fixed bucket size -- bucket count, and therefore
// this node's degree, stays capped at 4 no matter how large account count grows; reuses the SAME
// bucket node when multiple accounts land in the same bucket -- CREATE here would mint a fresh
// bucket every iteration instead of sharing one
MERGE (s:Status {label: 'verified'})
// => the ONE shared status node, reused across every bucket -- never duplicated
MERGE (g)-[:HAS_STATUS]->(s)
// => the bucket-to-status edge exists ONCE per bucket, not once per account
CREATE (:Account {name: 'Acc' + toString(i)})-[:IN_GROUP]->(g);
// => each account still gets its OWN fresh IN_GROUP edge into its bucket -- only the shared
// group/status nodes and the edge between them are merged, not the accounts themselves

MATCH (s:Status {label: 'verified'})
// => the SAME shared node the "before" form measured, for a like-for-like comparison
RETURN COUNT { (s)--() } AS status_degree;
// => status_degree is bounded by the FIXED bucket count (4) -- genuinely O(1) as account count
// grows, unlike the "before" form's unbounded 1-to-1 growth
