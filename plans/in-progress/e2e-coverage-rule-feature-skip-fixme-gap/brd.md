# Business Requirements: E2E Coverage Rule/Feature Skip/Fixme Gap

## Business Goal and Rationale

The `specs e2e-coverage validate` gate exists to mechanically catch silently-unbound e2e scenarios. A
structural blind spot in the detector itself (Rule/Feature-level `@skip`/`@fixme` invisible to it)
undermines the gate's core promise, even though it is currently dormant. Closing it now, while the
codebase has zero live usage of the affected tag shape, is strictly cheaper than closing it after a
future contributor adopts `Rule:`-level skip tags and ships an undetected gap.

## Business Impact

- **Pain point**: a future contributor who tags a `Rule:` block `@skip`/`@fixme` gets a false PASS
  from the gate — the exact failure mode this whole detector was built to prevent.
- **Expected benefit**: complete parity between Outline-level and Rule/Feature-level special-tag
  detection, closing the gate's only known remaining structural gap.

## Affected Roles

- Any contributor authoring Gherkin `.feature` files with `Rule:` blocks in a playwright-bdd-gated
  project.

## Success Metrics

- _Observable fact_: a new regression fixture (a `Rule:`-level `@skip`/`@fixme` tag with sibling
  non-skipped content) causes `specs:e2e:coverage` to FAIL before the fix and PASS after, mirroring
  the existing Outline-level regression test's structure.

## Business Scope Non-Goals

- Not a general re-audit of the entire e2e-coverage detector — scoped to the specific Rule/Feature gap
  identified by PR #66 cycle-7's review, plus the DD-6 doc-currency fix identified in the same cycle.

## Business Risks and Mitigations

- **Risk**: none identified beyond the standard risk of any parser-logic change (a false positive that
  breaks an existing passing project). **Mitigation**: run `nx run-many -t specs:e2e:coverage` across
  all 11 wired projects before merge, per this plan's precedent.
