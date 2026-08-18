# Mandatory Systematic Sweeps (Part 2)

## C. Declared-invariant conformance pass

Cross-cutting promises are the richest miss source because they must hold for **every** operation, not
a sample. Before and during the tour, extract the target's declared invariants and verify each holds
universally:

1. Discover invariants from ground truth the agent already reads — the OpenAPI spec / SDL (a global
   `security` requirement, a shared error `component`, a `nullable: false` field), `specs/**`, the plan
   docs, `CLAUDE.md`/`AGENTS.md`, and handler source headers (e.g. a middleware comment "all routes
   require a bearer token"; a rule "every timestamp is RFC 3339 UTC"; "every error is problem+json").
2. For each invariant, enumerate every operation it applies to and **assert it holds for ALL of them**
   — not the first few. A promise kept for most operations and broken for one is a finding citing the
   invariant as "expected".
3. List each invariant and its conformance verdict (holds / partial — with the offending operations) in
   the coverage map.

> Class this catches: _a "every endpoint enforces auth" promise that in fact left one debug route
> open._

## Self-completeness check (close the run)

Before writing up, run one explicit critic pass over the matrices: **"which operation, method, payload
edge, auth context, error path, or declared invariant did I NOT enumerate?"** Any blank cell is either
filled or recorded under "areas not covered" with the reason — silent omission reads as "all clear"
when it is not.
