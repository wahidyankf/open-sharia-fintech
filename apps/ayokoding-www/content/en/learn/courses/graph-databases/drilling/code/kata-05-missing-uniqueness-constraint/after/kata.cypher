// Kata 5 (after): CREATE CONSTRAINT rejects the second write outright.
CREATE CONSTRAINT person_name FOR (p:Person) REQUIRE p.name IS UNIQUE;
// THE FIX: the constraint must exist BEFORE the duplicate write is attempted

CREATE (:Person {name: 'Ada'});
// => succeeds -- first (and now GUARANTEED only) Person named Ada

CREATE (:Person {name: 'Ada'});
// => FAILS: Neo.ClientError.Schema.ConstraintValidationFailed -- rejected before writing
