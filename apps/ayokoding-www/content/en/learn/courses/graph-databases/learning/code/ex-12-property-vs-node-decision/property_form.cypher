// Example 12a: age as a PROPERTY.
CREATE (:Person {name: 'Ada', age: 36});
// => age lives directly on the node -- reading it costs zero hops

MATCH (p:Person {name: 'Ada'})
RETURN p.age;
// => one property read, no traversal at all
