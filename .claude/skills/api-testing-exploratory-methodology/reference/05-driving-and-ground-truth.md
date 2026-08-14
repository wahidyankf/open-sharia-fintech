# How to Drive the API, and Contract & Specs as Ground Truth / Spec-Gap Detection

## How to Drive the API

1. **Baseline (always available)** — `Bash curl -sS -D - -o - -w '\n%{http_code} %{time_total}s\n'` the
   documented operations for status, headers, body, and timing; fetch `/openapi.json` /
   `/swagger.json` when present; for GraphQL, `POST` an `__schema` introspection query to obtain the
   live SDL. Pipe JSON through `jq` to assert on shape and values rather than eyeballing.
2. **Edge & negative probes** — write request scripts (a shell loop of `curl` calls, or a small
   Node/`jq` harness) to `local-temp/` that exercise the boundary/malformed/auth-context matrix across
   every operation; capture each request (method, path, redacted headers, body) and its response
   (status, headers, body). Save captures a finding cites to the backlog plan's `evidence/` subfolder
   (named `phase-N-<operation>-<condition>.http` or `.json`), not `local-temp/` — they become
   committed proof a developer can inspect. Treat tooling absence gracefully — fall back to plain
   `curl` and record the limitation under "areas not covered".
3. **Ground-truth comparison** — `Read`/`Glob`/`Grep` the OpenAPI spec / SDL, `specs/**`, handler
   source, and generated contract types to decide whether observed behaviour is a defect (diverges
   from the contract/intent) or expected.
4. **Value correctness** — for any computed or derived field, independently recompute or cross-check
   against the spec; assert the _value_, not just its presence or type.

## Contract & Specs as Ground Truth & Spec-Gap Detection

An API has **two** layers of executable intent, and both outrank the agent's assumptions:

1. The **API contract** — the OpenAPI 3.x document (e.g. under
   `specs/apps/<product>/containers/contracts/`) or the GraphQL SDL. This is the precise shape promise.
2. The repo's **`specs/**` Gherkin** — the behavioural record (`specs/apps/**`for apps,`specs/libs/**`
   for libraries).

Treat both as first-class ground truth, and treat the live API as evidence about what they _should_
say.

### Compare live behaviour against the contract and existing specs

1. **Locate the contract** — find the OpenAPI/SDL for the target (named pointer, `specs/apps/<product>/`
   contracts folder, or a live `/openapi.json` / introspection result).
2. **Locate the relevant features** — `Glob`/`Grep` `specs/apps/<target>/**` (and `specs/libs/**` when
   the target consumes a shared lib) for `.feature` files whose scenarios map to the operations under
   test.
3. **Exercise each operation and each mapped scenario on the live target** and sort every check into
   one of three buckets:
   - **Covered + passing** — live behaviour matches the contract/scenario; record it in the coverage
     map.
   - **Covered + diverging** — live behaviour contradicts the contract or a scenario; this is a
     **defect**. File it in `findings.md` with the **Expected Result citing the contract clause**
     (`openapi.yaml › paths./activities.post.responses.400`) or the **scenario**
     (`path/to.feature › Scenario name`).
   - **Uncovered** — feeds gap detection below.
4. **Cite the ground truth, not an assumption** — when a contract clause or Gherkin scenario exists,
   the finding's "expected" MUST quote it; the contract/spec outranks the agent's guess.

### Detect behaviours that should be added to the specs

While touring the operations, the agent continually observes behaviours that the existing `specs/**`
do **not** describe. Each is a candidate **spec gap** — a scenario the specs ought to carry so the
behaviour is protected by the
[Specs & Gherkin Completeness rule](../../../../repo-governance/development/quality/feature-change-completeness.md).
**Edge-case behaviours are the richest source of gaps**: boundary handling, empty-collection responses,
error-envelope rules, auth-rejection codes, and validation rules are frequently correct in the running
API yet absent from the Gherkin. When an edge behaviour observed under the dimensions above is correct
and intended, propose it as a Gherkin scenario here rather than letting it stay unprotected.

Propose a gap only when the observed behaviour is:

- **Intended / correct** — not itself a defect. Defects go to `findings.md`, never `spec-gaps.md`. If
  unsure whether it is intended (e.g. an undocumented field that might be a leak), record it as an open
  question rather than a confident proposal.
- **Reproducible** — deterministic enough to express as Given/When/Then over a request/response.
- **In the target's responsibility** — owned by this app/lib, not a gateway or upstream dependency.

For each gap, draft a Gherkin scenario (use the `plan-writing-gherkin-criteria` Skill) and name the
target `specs/**` file — an existing `.feature` to extend or a new one to add. Every gap is a
**proposal for maintainer confirmation**: the agent asserts "this behaviour exists and is
unprotected", not "the spec is wrong". These land in `spec-gaps.md`.
