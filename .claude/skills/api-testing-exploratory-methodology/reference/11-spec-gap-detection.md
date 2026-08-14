# Detecting and Proposing Spec Gaps

## Detect behaviours that should be added to the specs

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
