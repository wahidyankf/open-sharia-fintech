// Example 29: UNWIND a List into Rows.
UNWIND [1, 2, 3] AS x
CREATE (:Number {value: x});
// => co-23: UNWIND expands the 3-element list into 3 separate rows -- CREATE then runs ONCE PER ROW

MATCH (n:Number) RETURN n.value ORDER BY n.value;
// => three SEPARATE nodes exist, one per list element
