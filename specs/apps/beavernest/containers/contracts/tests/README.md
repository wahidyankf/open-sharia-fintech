# tests — BeaverNest Contracts

Assertion-only contract guards for the `beavernest-contracts` OpenAPI spec. `readiness-contract.sh`
asserts the running `beavernest-be` readiness endpoint's response shape matches
[the parent contract](../README.md); it is not a test runner in its own right and carries no other
fixtures.
