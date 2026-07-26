// Example 20: Create a Uniqueness Constraint.
CREATE CONSTRAINT person_name FOR (p:Person) REQUIRE p.name IS UNIQUE;
// => co-22: from now on, no two :Person nodes can share the same p.name value

CREATE (:Person {name: 'Ada'});
// => succeeds -- first (and so far only) :Person named 'Ada'

CREATE (:Person {name: 'Ada'});
// => FAILS: Neo.ClientError.Schema.ConstraintValidationFailed
// => the constraint rejects the duplicate BEFORE it is ever written, not after
