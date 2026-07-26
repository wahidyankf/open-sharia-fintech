// Example 2: Create a Node with Multiple Labels.
// Two labels, back-to-back with no comma, both apply to the SAME node (co-01).
CREATE (:Person:Engineer {name: 'Grace'});
// => one node, carrying BOTH labels at once -- not two nodes, not a subtype relationship

// A WHERE clause can require BOTH labels on the same node.
MATCH (n)
WHERE n:Person AND n:Engineer
RETURN n;
// => matches the one node above -- if it were missing either label this would return zero rows
