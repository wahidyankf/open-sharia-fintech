// Example 72b: AFTER -- accounts are bucketed through intermediate GROUP nodes first. (co-17, co-11)
UNWIND range(1, 5) AS i
// => the SAME 5 accounts as the "before" form, for a direct comparison
MERGE (g:VerifiedGroup {bucket: toInteger(i / 3)})
// => reuses the SAME bucket node when multiple accounts land in the same bucket -- CREATE here
// would mint a fresh bucket every iteration instead of sharing one
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
// => status_degree stays SMALL and roughly constant as account count grows -- unlike the "before" form
