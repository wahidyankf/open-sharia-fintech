// Example 72b: AFTER -- accounts are bucketed through intermediate GROUP nodes first. (co-17, co-11)
UNWIND range(1, 5) AS i
// => the SAME 5 accounts as the "before" form, for a direct comparison
CREATE (:Account {name: 'Acc' + toString(i)})
      -[:IN_GROUP]->(:VerifiedGroup {bucket: toInteger(i / 3)})
      // => each account joins a SMALL bucket first, instead of the shared node directly
      -[:HAS_STATUS]->(:Status {label: 'verified'});
// => each Account connects to a SMALL bucket node first -- the shared "verified" node's direct
// degree is now bounded by the NUMBER OF BUCKETS, not the number of accounts

MATCH (s:Status {label: 'verified'})
// => the SAME shared node the "before" form measured, for a like-for-like comparison
RETURN size((s)--()) AS status_degree;
// => status_degree stays SMALL and roughly constant as account count grows -- unlike the "before" form
