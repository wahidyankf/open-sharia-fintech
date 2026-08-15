# Product Requirements Document — Skills Path: ERP Enterprise Depth (Stage B + Stage C)

## Product Overview

Grows `skills/conventional-erp` (15 → 27 ids, terminal) and `skills/sharia-erp` (15 → 27 → 30 ids,
terminal). Both promise the reader the ability to **read, reason about, and design** an ERP system to
build-founding depth — never to operate, install, evaluate, or select one (A6/A7). This plan carries
both paths from their Stage A checkpoint to full domain competence.

## Personas

### Persona 1 — the systems-adjacent engineer (both paths)

Already walked plan 17's Stage A. Values the Dangerous 2 boundary (course 16 of 27/30) as the point
where the full subledger-to-GL relationship (P2P/O2C/R2R) and the hard parts of inventory are
explainable in practice.

### Persona 2 — the finance/ops professional moving into systems (both paths)

Values the explicit accounting-prerequisite edges this plan links (never duplicates) into the three
accounting-split plans, and the honest framing that Stage B teaches architecture, not accounting
itself.

### Persona 3 — the Sharia-compliance-focused reader (`sharia-erp` only)

Reaches this plan's Stage C to get the jurisdiction-plural Sharia-compliant design depth that plan 17's
Stage A explicitly deferred. Values the Dangerous 4 terminal boundary and the honest statement that
`sharia-erp` never required `conventional-erp` first — a promise plan 17 could not yet fully redeem at
its own 15-course checkpoint (where the two paths were identical) but this plan's terminal state does.

## Product Scope

**In scope**: 15 additional course bodies, both manifests grown to their terminal state, both
landings updated through Dangerous 2/3/4, 15 additional syllabus files, the Sharia-specific licensing
addendum, and Gherkin coverage for every remaining boundary.

**Out of scope**: any UI component (plan 03), any accounting content (the accounting-split plans), any
Stage A course or syllabus file (plan 17's exclusive scope), any build/install/evaluate/select content
(A6/A7).

## User Stories

- As the systems-adjacent engineer, I want to read `erp-subledger-to-gl-architecture`'s continuation
  into `record-to-report-systems` and immediately understand why a reconciliation break is invisible
  to a trial balance, so that I can design an integration that never bypasses a control account.
- As the finance/ops professional, I want `record-to-report-systems` to explicitly state its hard
  dependency on `financial-statements-and-close-cycle`, so that I know exactly which accounting
  competence I need before starting Stage B.
- As the Sharia-compliance-focused reader, I want the `sharia-erp` landing to state, once this plan's
  Stage C ships, that I never needed `conventional-erp` first, so that I don't waste time hunting for
  a different "start here" course.
- As any reader on either path, I want the Dangerous 2/3/4 boundaries to tell me honestly what I can
  and cannot yet reason about, so that I don't overestimate my own competence mid-path.

## Gherkin Scenarios

```gherkin
Feature: Skills ERP paths — Stage B/C growth to terminal state

  Scenario: the shared 27 courses are identical bodies referenced from both manifests
    Given a course id present in both "skills/conventional-erp" and "skills/sharia-erp" courseOrder
    When the reader visits that course under either path context
    Then the rendered body content is byte-identical
    And no second copy of the course file exists on disk

  Scenario: conventional-erp manifest validates against the PathManifest schema at its terminal 27 ids
    Given the file "manifests/skills/conventional-erp.json"
    When the manifest is loaded and validated
    Then it parses against the PathManifest zod schema
    And its pathId equals "skills/conventional-erp"
    And its arc equals "immediately-effective"
    And its courseOrder contains exactly 27 unique course ids

  Scenario: sharia-erp manifest validates against the PathManifest schema at its terminal 30 ids
    Given the file "manifests/skills/sharia-erp.json"
    When the manifest is loaded and validated
    Then it parses against the PathManifest zod schema
    And its pathId equals "skills/sharia-erp"
    And its courseOrder contains exactly 30 unique course ids
    And its courseOrder position 27 equals "erp-analytics-and-reporting"
    And its courseOrder positions 28 to 30 are the 3 Sharia-exclusive ids in catalog order
    And its final courseOrder entry equals "zakat-and-sharia-compliance-modules"

  Scenario: conventional-erp landing renders with its full terminal course count
    Given the reader navigates to "/en/learn/paths/skills/conventional-erp"
    When the landing page loads
    Then the landing renders 27 courses in courseOrder order
    And the landing displays the Dangerous 1, Dangerous 2, and Dangerous 3 boundaries
    And the landing states "ENDS HERE" at Dangerous 3

  Scenario: sharia-erp landing renders with its full terminal course count and states it covers the basics
    Given the reader navigates to "/en/learn/paths/skills/sharia-erp"
    When the landing page loads
    Then the landing renders 30 courses in courseOrder order
    And the landing displays the Dangerous 1 through Dangerous 4 boundaries
    And the landing states explicitly that the path covers all the basics without requiring
      "conventional-erp" first

  Scenario: record-to-report-systems declares its hard accounting prerequisite
    Given the course "record-to-report-systems"
    When its frontmatter is inspected
    Then its frontmatter prerequisites include "financial-statements-and-close-cycle"

  Scenario: production-planning-and-mrp cites plan 17's erp-bom-and-routing-architecture by id
    Given the course "production-planning-and-mrp"
    When its frontmatter is inspected
    Then its frontmatter prerequisites include "erp-bom-and-routing-architecture"

  Scenario: no course id, path id, or landing title contains a vendor trademark
    Given every course id in this plan's 15-course slice and both path ids
    When every id is scanned
    Then none of them matches "sap", "oracle", "netsuite", "erpnext", or "odoo" (case-insensitive)

  Scenario: the two scope-boundary-risk courses in this plan's slice each carry a self-check
    Given the courses "erp-analytics-and-reporting" and "erp-security-and-controls"
    When each course's overview is inspected
    Then each contains a worked example distinguishing its ERP-specific scope from its named
      general-purpose existing-library sibling course

  Scenario: prerequisite consistency holds across both manifests together at terminal state
    Given both "skills/conventional-erp" and "skills/sharia-erp" manifests at their terminal ids
    When checkPrerequisiteConsistency runs against both
    Then it reports zero violations

  Scenario: conventional-erp is verified unchanged while sharia-erp grows to Stage C
    Given "skills/conventional-erp" already reached its terminal 27 ids at the end of Stage B
    When "skills/sharia-erp" grows from 27 to 30 ids in Stage C
    Then "skills/conventional-erp"'s courseOrder is byte-identical before and after Stage C growth

  Scenario: a reader entering sharia-erp cold reaches Dangerous 1 without visiting conventional-erp
    Given a reader who has never visited "skills/conventional-erp"
    When they complete the first 9 courses of "skills/sharia-erp" in courseOrder
    Then they reach the same Dangerous 1 capability boundary as a conventional-erp reader would
```

## Ramp Boundary Language (re-grounded)

Every "Dangerous N" boundary is phrased as what the reader can **read, reason about, and design** —
never "operate", "install", or "configure a live system" — carried forward unchanged from plan 17 and
the retired source plan.

## UI-Design-Funnel Exemption

This plan ships no net-new screen or component. Every screen its output appears on is designed,
mocked, and rendered by `ayokoding-learning-path-03-navigation-ui`. See
[tech-docs.md §UI-design-funnel exemption](./tech-docs.md#ui-design-funnel-exemption-recorded-explicitly).

## Product-Level Risks

- **A reader who completed only plan 17's Stage A misjudges the successor plan's growth as a
  different product.** Mitigated by both landings' content updating in place — same URL, same
  manifest file, growing `courseOrder` — never a new path id.
- **A reader assumes `sharia-erp` requires `conventional-erp` first**, even after this plan's Stage C
  ships. Mitigated by the terminal L-5 landing statement, reinforced by `courseOrder` actually
  including all 27 shared ids ahead of the 3 Sharia-exclusive ones.
- **The Dangerous-N ramp table fails to render legibly across breakpoints** once it carries four
  named boundaries plus their course-id anchors. Mitigated by this plan's own Phase 6 manual
  verification gate, screenshotting each path landing at three breakpoints.
- **A reader over-trusts the Dangerous-N framing as operational competence.** Mitigated by the
  re-grounded phrasing never using "operate", "install", or "configure a live system" language at any
  boundary.
