# Product Requirements — Learning-Plan `syllabus/` Folder Convention

## Product Overview

A governance product with four parts, all delivered as markdown:

1. **A convention document** — `repo-governance/conventions/structure/learning-plan-syllabus.md` —
   defining what makes a plan **learning-bearing**, the required `syllabus/` folder layout, the
   per-course file shape, the **Corpus Disposition** rule, and the **custody** rule.
2. **A copy-paste course template**, embedded as a fenced block in that convention and derived from
   the measured section census of the 174 existing course files `[Repo-grounded]`.
3. **Enforcement wiring** across `plan-maker` → `plan-checker` → `plan-fixer`, the
   `plan-creating-project-plans` skill, and the `plan-quality-gate` workflow — the same chain that
   already carries the UI-design-funnel rule.
4. **A conformance recipe** — runnable `grep` commands an author or checker applies today — plus a
   two-pager filing the deterministic validator as future work.

**This plan is not UI-bearing.** It adds and changes no user-facing screen or component under
`apps/` or `libs/`; every artifact is a markdown governance file. The UI-design-funnel requirement is
therefore exempt, and the exemption is restated in
[tech-docs.md §Exemptions](./tech-docs.md#exemptions-declared).

## Personas

| Persona                          | Hat / agent                                                        | What they need from this product                                              |
| -------------------------------- | ------------------------------------------------------------------ | ----------------------------------------------------------------------------- |
| **Course architect**             | Maintainer authoring a learning-bearing plan                       | A template to copy, so the format is inherited rather than reverse-engineered |
| **Corpus consumer**              | Maintainer/agent authoring a plan that reads someone else's corpus | A written statement of what they may and may not touch                        |
| **`plan-maker`**                 | Planning agent                                                     | A trigger definition and a list of artifacts to require                       |
| **`plan-checker`**               | Validation agent                                                   | A completeness step with concrete, greppable pass/fail conditions             |
| **`plan-fixer`**                 | Remediation agent                                                  | A scaffold shape to write into a plan missing the record                      |
| **Future conformance validator** | Deterministic `rhino-cli` check (not built here)                   | A settled, written format to validate against                                 |

## User Stories

- **US-1** — As a **course architect**, I want a copy-paste course template in a convention, so that
  I author a conforming syllabus without reading and reverse-engineering an existing sample.
- **US-2** — As a **course architect**, I want the `syllabus/` folder layout written down, so that
  `courses/` and `paths/` are not re-invented per plan.
- **US-3** — As **`plan-checker`**, I want a learning-bearing completeness step, so that a plan which
  authors course content but ships no syllabus record fails the gate instead of passing silently.
- **US-4** — As a **corpus consumer**, I want a written custody rule, so that I know I may read but
  not edit a corpus another plan owns, and where to route an edit I need.
- **US-5** — As a **maintainer archiving a custodian plan**, I want a written disposition rule, so
  that I know before pushing whether the corpus moves, stays, or blocks archival.
- **US-6** — As a **maintainer of the existing corpora**, I want the convention derived from the
  files that exist, so that adopting it costs no reformatting of 174 course files.
- **US-7** — As a **checker or author**, I want a runnable conformance recipe, so that I can detect a
  missing required section today without waiting for a deterministic validator.

## Acceptance Criteria (Gherkin)

```gherkin
Feature: Learning-bearing plans carry a governed syllabus

  Scenario: A learning-bearing plan without a syllabus record fails the gate
    Given a plan whose delivery checklist authors or restructures course or tutorial content
    And that plan has no "syllabus/" folder and no "## Corpus Disposition" declaration
    When plan-checker runs its learning-bearing completeness step
    Then the checker reports a HIGH finding naming each missing artifact
    And the plan-quality-gate does not reach a pass verdict at strict mode

  Scenario: A learning-bearing plan with a complete syllabus record passes
    Given a plan carrying "syllabus/courses/" and "syllabus/paths/"
    And its "syllabus/README.md" names a custodian and its "tech-docs.md" declares a Corpus Disposition
    When plan-checker runs its learning-bearing completeness step
    Then the checker reports zero findings for that step
    And the plan-quality-gate verdict is unaffected by the learning-bearing check

  Scenario: A plan that authors no learning content is exempt
    Given a plan whose scope touches only governance documents and agent definitions
    When plan-checker evaluates the learning-bearing trigger
    Then the checker records the plan as exempt
    And no syllabus finding is emitted

  Scenario: An author copies the template instead of a sample
    Given the convention at repo-governance/conventions/structure/learning-plan-syllabus.md
    When an author reads its course-template section
    Then a single fenced block contains every REQUIRED section with placeholder content
    And each RECOMMENDED and OPTIONAL section is labelled with the tier it belongs to

  Scenario: The default corpus disposition keeps the corpus in the plan folder
    Given a learning-bearing plan whose corpus has no consumer outside plans/
    When the plan declares its Corpus Disposition
    Then the declared value is "archive-with-plan"
    And the corpus moves to plans/done/ with the plan folder on archival

  Scenario: A non-plan consumer forces promotion out of plans/
    Given a corpus that a checker, generator, or build step outside plans/ reads
    When the custodian plan declares its Corpus Disposition
    Then the declared value is "promote-to:<path>" naming a durable home outside plans/
    And the delivery checklist carries a step performing the move and rewriting inbound links

  Scenario: A consumer plan may read but not edit a corpus it does not custody
    Given plan A custodies a corpus and plan B links into it
    When plan B needs a change to a file in that corpus
    Then plan B records the change as a request routed to plan A's delivery checklist
    And plan B's own delivery checklist contains no step editing a file under plan A's syllabus

  Scenario: Archiving a custodian with a live consumer requires a hand-off
    Given a custodian plan ready to archive while a live consumer still links into its corpus
    When the archival step runs
    Then the checklist rewrites every inbound link to the corpus's new location or transfers custody to a named successor plan
    And "rhino-cli md links validate" exits 0 afterwards

  Scenario: Existing course files are grandfathered, not reformatted
    Given the 17 plan-02 course files that render concepts as an ordered list
    When the convention lands
    Then no delivery step edits the body of any existing course file
    And the convention names that cohort as explicitly grandfathered

  Scenario: The conformance recipe detects a missing required section
    Given a course file lacking the "## Concepts" section
    When the convention's documented grep recipe runs over the corpus
    Then the recipe reports that file
    And the recipe's own documented invocation exits non-zero for that corpus
```

## Product Scope

### In scope

- The convention document, its course template, its Corpus Disposition rule, and its custody rule.
- The learning-bearing trigger definition, phrased to parallel the UI-bearing trigger.
- Enforcement wiring in `plan-maker`, `plan-checker`, `plan-fixer`, the
  `plan-creating-project-plans` skill, and the `plan-quality-gate` workflow, plus the regenerated
  platform bindings.
- Index updates: `repo-governance/conventions/structure/README.md`,
  `repo-governance/conventions/README.md`, and a cross-reference from
  `repo-governance/conventions/structure/plans.md`.
- Declaring custodian and disposition for the three existing corpora, and adding the consumer-side
  custody note to plans 04 and 05.
- A documented conformance recipe and a two-pager filing the deterministic validator.

### Out of scope

- Reformatting, moving, or renaming any existing course or manifest file.
- Building the deterministic `rhino-cli` conformance validator.
- Any change to the UI-design-funnel rule, `assets/`, or `diagrams.md` beyond a one-line
  cross-reference if the checker step numbering requires it.
- Authoring course bodies, changing the course catalog, or touching `apps/ayokoding-www/content/`.
- Moving any existing corpus out of `plans/`.
- Propagating anything under `plans/` to `ose-primer` / `ose-infra` — the `ayokoding-learning-path-*`
  corpora and their custody declarations are `ose-public` content with no sibling counterpart.
  Propagation of the convention and its enforcement **is** in scope; see `DD-12` and Phase 6.

## Product Risks

| Risk                                                                                              | Severity | Mitigation                                                                                                                                                       |
| ------------------------------------------------------------------------------------------------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| The REQUIRED tier is drawn too wide and rejects legitimate non-course learning content            | HIGH     | REQUIRED is limited to sections present in ≥ 99% of files across **all three** corpora; everything else is RECOMMENDED or OPTIONAL                               |
| The learning-bearing trigger is ambiguous, so checkers fire on plans that merely mention a course | MEDIUM   | The trigger is defined by delivery-step effect ("authors or restructures course/tutorial content"), with worked positive and negative examples in the convention |
| The custody rule is unenforceable and becomes decoration                                          | MEDIUM   | The link-integrity half is already mechanically enforced by `md links validate` at pre-push and CI; the convention names that backstop explicitly                |
| Enforcement wiring drifts between `.claude/` and `.opencode/` mirrors                             | LOW      | Bindings are regenerated with `npm run generate:bindings`, never hand-edited, and the phase gate verifies the mirrors                                            |
| A fourth learning-bearing plan lands mid-execution and forks again                                | LOW      | Phase 1 delivers the convention and template before any wiring work, so the artifact an author can copy exists as early as possible                              |

## Related Documents

- [brd.md](./brd.md) — the business claims these scenarios test
- [tech-docs.md](./tech-docs.md) — the census, the design decisions, and the template tiering
- [delivery.md](./delivery.md) — the phased execution checklist
