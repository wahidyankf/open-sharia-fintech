# Specs as Ground Truth & Spec-Gap Detection

The repo's `specs/**` tree is the executable record of intended behaviour (`specs/apps/**` for apps,
`specs/libs/**` for libraries). Treat it as a first-class ground truth alongside the design mockups —
and treat the live site as evidence about what the specs _should_ say.

## Compare live behaviour against existing specs

1. **Locate the relevant features** — `Glob`/`Grep` `specs/apps/<target>/**` (and `specs/libs/**`
   when the target consumes a shared lib) for `.feature` files whose scenarios map to the URL(s) and
   flows under test.
2. **Exercise each mapped scenario on the live target** — walk its Given/When/Then against the
   running site and sort every scenario into one of three buckets:
   - **Covered + passing** — live behaviour matches the scenario; record it in the `README.md`
     coverage map.
   - **Covered + diverging** — live behaviour contradicts the scenario; this is a **defect**. File it
     in `findings.md` with the **Expected Result citing the scenario** by
     `path/to.feature › Scenario name`.
   - **Uncovered** — feeds gap detection below.
3. **Cite the spec, not an assumption** — when a Gherkin scenario exists, the finding's "expected"
   MUST quote it; the spec outranks the agent's guess about correct behaviour.

## Detect behaviours that should be added to the specs

While touring the URL(s) / location, the agent continually observes behaviours that the existing
`specs/**` do **not** describe. Each is a candidate **spec gap** — a scenario the specs ought to
carry so the behaviour is protected by the
[Specs & Gherkin Completeness rule](../../../../repo-governance/development/quality/feature-change-completeness.md).
**Edge-case behaviours are the richest source of gaps**: boundary handling, empty/zero-result states,
error recovery, and input-validation rules are frequently correct in the running app yet absent from
the spec. When an edge behaviour observed under the dimensions checklist is correct and intended,
propose it as a Gherkin scenario here rather than letting it stay unprotected.

Propose a gap only when the observed behaviour is:

- **Intended / correct** — not itself a defect. Defects go to `findings.md`, never `spec-gaps.md`. If
  unsure whether it is intended, record it as an open question rather than a confident proposal.
- **Reproducible** — deterministic enough to express as Given/When/Then.
- **In the target's responsibility** — owned by this app/lib, not a third-party widget or the
  browser.

For each gap, draft a Gherkin scenario (use the `plan-writing-gherkin-criteria` Skill) and name the
target `specs/**` file — an existing `.feature` to extend or a new one to add. Every gap is a
**proposal for maintainer confirmation**: the agent asserts "this behaviour exists and is
unprotected", not "the spec is wrong". These land in `spec-gaps.md`.
