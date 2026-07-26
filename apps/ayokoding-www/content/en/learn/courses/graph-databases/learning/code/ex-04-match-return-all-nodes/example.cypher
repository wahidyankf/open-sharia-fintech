// Example 4: Match and Return All Nodes.
// Seed three nodes first -- this example is self-contained, like every other one.
CREATE (:Person {name: 'Ada'});
// => first of three seeded people
CREATE (:Person {name: 'Grace'});
// => second seeded person
CREATE (:Person {name: 'Alan'});
// => third seeded person -- three :Person nodes now exist, zero relationships between them

// MATCH / WHERE / RETURN (co-05) is Cypher's core read pipeline: pattern-match, filter, project.
MATCH (n)
// => matches EVERY node in the database -- no label, no WHERE filter narrows this yet
RETURN n
// => projects the whole node back, unfiltered
LIMIT 25;
// => returns all 3 nodes -- LIMIT 25 is a safety cap, not a filter that trims real results here
