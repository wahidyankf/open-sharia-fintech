# Mandatory Systematic Sweeps (Part 1)

The dimension checklist gives **breadth**; these three sweeps give **exhaustiveness**. They are not
optional charters — every `standard` and `thorough` run MUST execute all three and record their
matrices in the `README.md` coverage map. They exist because dimension-and-tour testing reliably finds
_representative_ defects yet repeatedly misses the **"enumerate every operation and assert one
property"** class: a list endpoint that ignores its own pagination contract, an error path that returns
a different envelope, an auth check present on nine operations and missing on the tenth.
**Enumerate; do not sample.** A sampled or empty matrix is not coverage.

## A. Operation × property matrix (contract conformance by enumeration)

1. Enumerate EVERY documented operation from the contract — each OpenAPI path×method, or each GraphQL
   query/mutation field. When no contract is given, enumerate every operation discovered live.
2. For each operation, exercise a representative valid request and assert the conformance properties:
   correct success status, response body matches the declared schema/type, declared headers present,
   declared content-type returned.
3. Record the matrix (operation rows × {status / schema / headers / content-type} columns,
   ✓ / ✗ / n-a per cell) in the coverage map. A blank cell is uncovered, not passing.

> Class this catches: _"the schema for `GET /activities/{id}` documents `createdAt` but the live
> response omits it on records created before the migration."_

## B. Cross-cutting convention round-trip sweep

For EVERY convention the API declares once but must honour everywhere — error envelope, pagination
params, auth requirement, timestamp/ID format, sort syntax:

1. Identify the convention and the set of operations it applies to.
2. Exercise the convention on each operation in that set (e.g. send a bad payload to every write
   endpoint and compare error envelopes; request page 2 from every list endpoint).
3. Assert the convention holds **uniformly** — a convention honoured for nine operations and broken for
   the tenth is a Major+ consistency defect citing a conforming operation as "expected".
4. Record a convention × operation table (✓ / ✗ / n-a) in the coverage map.

> Class this catches: _"every list endpoint paginates except `GET /tags`, which returns the unbounded
> set and ignores `?page`."_
