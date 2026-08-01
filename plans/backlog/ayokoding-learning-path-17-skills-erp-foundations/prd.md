# Product Requirements Document — Skills Path: ERP Foundations (Stage A)

## Product Overview

Publishes `skills/conventional-erp` and `skills/sharia-erp` at **15 course ids each** — the shared
Stage A foundation both paths' terminal 27/30-course states will build on. Both promise the reader the
ability to **read, reason about, and design** an ERP system to build-founding depth — never to
operate, install, evaluate, or select one (A6/A7) — up through the Dangerous 1 boundary this plan
reaches.

## Personas

### Persona 1 — the systems-adjacent engineer (both paths)

A software engineer who will build against, extend, or integrate with an ERP but has never worked
inside one. Enters at course 1, values the Dangerous 1 boundary (course 9) as the point where they can
start reviewing a real system's document/posting/account-determination design critically.

### Persona 2 — the finance/ops professional moving into systems (both paths)

Someone with accounting or operations background who wants to understand how the systems that
implement those processes are architected. At this plan's own boundary they get the architecture
spine only — the accounting-linked depth (subledger-to-GL, costing, close) is the successor plan's
Stage B.

### Persona 3 — the Sharia-compliance-focused reader (`sharia-erp` only)

Wants ERP domain literacy specifically for Sharia-compliant deployments. At this plan's checkpoint,
`sharia-erp` and `conventional-erp` are **identical** (both hold the same 15 Stage A ids) — the
Sharia-specific depth arrives only in the successor plan's Stage C. The `sharia-erp` landing states
this plainly rather than implying a difference that does not yet exist.

## Product Scope

**In scope**: 15 course bodies, 2 manifests published fresh at 15 ids, 2 landings (content spec
only) through the Dangerous 1 boundary, 15 syllabus files, the general ERP licensing section, and
Gherkin coverage for the Dangerous 1 milestone.

**Out of scope**: any UI component (plan `03`), any accounting content (the accounting-split plans),
any Stage B/C course (the successor plan), any build/install/evaluate/select content (A6/A7).

## User Stories

- As the systems-adjacent engineer, I want to read `erp-module-map-and-architecture` and immediately
  understand how the FI/CO/MM/SD modules relate, so that I can review a real system's module boundary
  choices critically.
- As the finance/ops professional, I want the landing to state honestly that the 9-course runway to
  Dangerous 1 is architecture, not padding, so that I understand why the boundary lands later than
  the sibling accounting path's does.
- As the Sharia-compliance-focused reader, I want the `sharia-erp` landing to state that it is
  identical to `conventional-erp` at this checkpoint and will diverge only once the successor plan's
  Stage C ships, so that I am not confused about what "Sharia-compliant" currently buys me.
- As any reader on either path, I want the Dangerous 1 boundary to tell me honestly what I can and
  cannot yet reason about, so that I don't overestimate my own competence this early in the ramp.

## Gherkin Scenarios

```gherkin
Feature: Skills ERP paths — Stage A publication and Dangerous 1 boundary

  Scenario: Stage A landings render and both manifests validate at 15 courses
    Given both manifests are published with courseOrder containing the 15 Stage A ids
    When a reader opens either the conventional-erp or sharia-erp path landing
    Then both landings render and both manifests validate against the PathManifest schema
    And the Dangerous-1 boundary appears correctly on both landings

  Scenario: conventional-erp manifest validates against the PathManifest schema at 15 ids
    Given the file "manifests/skills/conventional-erp.yaml"
    When the manifest is loaded and validated
    Then it parses against the PathManifest zod schema
    And its pathId equals "skills/conventional-erp"
    And its arc equals "immediately-effective"
    And its courseOrder contains exactly 15 unique course ids

  Scenario: sharia-erp manifest validates against the PathManifest schema at 15 ids
    Given the file "manifests/skills/sharia-erp.yaml"
    When the manifest is loaded and validated
    Then it parses against the PathManifest zod schema
    And its pathId equals "skills/sharia-erp"
    And its courseOrder contains exactly 15 unique course ids
    And its courseOrder is identical to "skills/conventional-erp"'s courseOrder at this checkpoint

  Scenario: the 15 shared courses are identical bodies referenced from both manifests
    Given a course id present in both "skills/conventional-erp" and "skills/sharia-erp" courseOrder
    When the reader visits that course under either path context
    Then the rendered body content is byte-identical
    And no second copy of the course file exists on disk

  Scenario: sharia-erp landing states it is identical to conventional-erp at this checkpoint
    Given the reader navigates to "/en/learn/paths/skills/sharia-erp"
    When the landing page loads at the Stage A checkpoint
    Then the landing states explicitly that all 15 published courses are shared with
      "conventional-erp" and that Sharia-specific depth arrives in a later release

  Scenario: no course id, path id, or landing title contains a vendor trademark
    Given every course id in this plan's 15-course slice and both path ids
    When every id is scanned
    Then none of them matches "sap", "oracle", "netsuite", "erpnext", or "odoo" (case-insensitive)

  Scenario: the erp-extension-and-customization scope-boundary self-check is present
    Given the course "erp-extension-and-customization"
    When its overview is inspected
    Then it contains a worked example distinguishing its ERP-specific scope from
      "sql-essentials"'s general-purpose scope

  Scenario: prerequisite consistency holds across both manifests together
    Given both "skills/conventional-erp" and "skills/sharia-erp" manifests at 15 ids
    When checkPrerequisiteConsistency runs against both
    Then it reports zero violations

  Scenario: erp-bom-and-routing-architecture is authored despite its late reading position
    Given the course "erp-bom-and-routing-architecture"
    When its frontmatter is inspected
    Then its prerequisites include only "erp-conceptual-data-model"
    And it declares no accounting or Stage B/C prerequisite
```

## Product-Level Risks

- **A reader confuses the two manifests as meaningfully different at this checkpoint.**
  `sharia-erp` and `conventional-erp` are byte-identical through all 15 Stage A ids — nothing yet
  distinguishes them. Mitigated by the DD-10 landing statement (see
  [tech-docs.md §Design Decisions](./tech-docs.md#design-decisions)) that names the identity
  explicitly instead of implying Sharia-specific depth that does not yet exist.
- **A reader grows impatient with the 9-course runway to Dangerous 1**, expecting a quicker payoff
  than the sibling accounting path's boundary. Mitigated by Requirement L-2's on-landing
  justification — the architecture spine has no smaller usable subset — stated to the reader rather
  than hidden in planning docs only.
- **A reader over-estimates their own competence once they cross Dangerous 1**, treating "can read
  and reason about" as "can operate a live system." Mitigated by Requirement L-1's explicit
  can/cannot framing on both landings, and by the ramp language never using "operate", "install", or
  "configure a live system" (carried forward from the retired source plan's re-grounded phrasing).
- **A reader on the `sharia-erp` path assumes it requires visiting `conventional-erp` first.**
  Mitigated by the Gherkin scenario proving a cold `sharia-erp` entrant reaches the same Dangerous 1
  boundary independently, and by both landings sharing identical `courseOrder` at this checkpoint.
- **The Persona 3 story's Sharia-identity framing reads as marketing rather than an honest
  disclosure.** Mitigated by stating the identity plainly on the `sharia-erp` landing itself (DD-10),
  not deferring the caveat to fine print.
