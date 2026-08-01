# PRD: Plan Decision-Integrity Hardening

## Product overview

Four authoring-time rules for plan documents, one mechanical checker step that enforces them, a
parity backfill of five orphaned governance routings, a post-mortem, and a retroactive pass over
every open plan in three repositories.

The product is a change to how plans are written and validated. It ships as edits to governance
conventions, three plan-lifecycle agent definitions, one skill, one post-mortem document, and the
open plan folders themselves. No application or library source is touched.

## Personas

The maintainer wears every hat below; the agents are literal consumers of the changed files.

| Persona                      | Need                                                                                                   |
| ---------------------------- | ------------------------------------------------------------------------------------------------------ |
| **Plan author** (maintainer) | To find out at authoring time that a design selection loses its own job criterion, not two plans later |
| **`plan-maker`**             | An unambiguous statement of which sections to emit and which question to grill, per rule               |
| **`plan-checker`**           | Enumerated, mechanically-evaluable clauses with fixed severities, so the scan is reproducible          |
| **`plan-fixer`**             | A named scaffold per finding, so a flagged plan can be repaired without re-deriving the rule           |
| **Future plan reader**       | To understand why a design was chosen, including when a later plan reversed it and on what basis       |
| **Repo governance owner**    | Provable three-repo parity, checked the same way the original drift was detected                       |

## User stories

- **US-1** — As a **plan author**, I want the Justify table to force one named job criterion, so that
  a selection that loses the page's actual purpose cannot be recorded as a clean win.
- **US-2** — As a **plan author**, I want fidelity to my own phrasing of a solution to be
  inadmissible as a criterion, so that the funnel tests the solution instead of confirming it.
- **US-3** — As a **plan author**, I want an option's elimination to require the artefact that proves
  the drop reason, so that I cannot narrow the design space on an untested assertion.
- **US-4** — As a **future plan reader**, I want a plan that reverses a predecessor to say which
  decision it reverses and why the original reason no longer holds, so that the reversal is legible
  as a decision rather than as drift.
- **US-5** — As a **plan author**, I want a closed set of user-visible identifiers to be checked for a
  consistent naming rule at schema-design time, so that a rename costs one file instead of six binding
  surfaces.
- **US-6** — As **`plan-checker`**, I want each rule expressed as a clause with a fixed severity and a
  named escape, so that I neither miss violations nor block legitimate exceptions.
- **US-7** — As a **repo governance owner**, I want every governance routing to reach all three repos
  in the same change, so that a rule written to prevent a recurrence is not itself an example of the
  drift it describes.
- **US-8** — As a **plan author with work already open**, I want existing plans brought into
  compliance rather than grandfathered, so that a currently-open UI plan cannot ship the defect the
  week after the rules land.

## Acceptance criteria

Every scenario uses exactly one primary `Given`, one `When`, and one `Then`; additional steps chain
with `And`.

### R-A — Primary Job Criterion

```gherkin
Scenario: AC-1 A UI-bearing plan's Justify table names exactly one Primary Job Criterion
  Given a UI-bearing plan whose prd.md contains a Stage-4 Justify table
  When plan-checker runs Step 5o against the plan
  Then the scan passes only if exactly one criterion row is marked as the Primary Job Criterion
  And a table with zero such rows is reported as HIGH
  And a table with two or more such rows is reported as HIGH
```

```gherkin
Scenario: AC-2 The Primary Job Criterion is traceable to a stated problem
  Given a UI-bearing plan whose Justify table marks a Primary Job Criterion row
  When plan-checker evaluates that row
  Then the scan passes only if the row cites an anchor in the plan's own brd.md
  And a Primary Job Criterion citing no brd.md anchor is reported as MEDIUM
```

```gherkin
Scenario: AC-3 A criterion phrased as fidelity to the requester's wording is inadmissible
  Given a Justify table containing a criterion row whose text matches a requester-phrasing pattern
  When plan-checker evaluates the table
  Then that row is reported as MEDIUM with the matched phrase quoted
  And the finding names the rule that forbids scoring a candidate solution against its own description
```

```gherkin
Scenario: AC-4 A selection that loses the Primary Job Criterion without an override is flagged
  Given a Justify table whose Primary Job Criterion row is won by an option other than the selected one
  When plan-checker evaluates the table and finds no Primary Job Criterion Override Record
  Then the scan reports HIGH
  And the finding names both the selected option and the option that won the criterion
```

```gherkin
Scenario: AC-5 A selection that loses the Primary Job Criterion with a written override passes
  Given a Justify table whose Primary Job Criterion row is won by an option other than the selected one
  When plan-checker finds a Primary Job Criterion Override Record immediately below the table
  Then the scan passes for that clause
  And the record is required to name the winning option, the reason for selecting otherwise, and the recorded user decision
```

### R-B — Elimination-Grade Evidence

```gherkin
Scenario: AC-6 An option dropped on a breakpoint claim with no artefact at that width is flagged
  Given a funnel whose drop reason for an option names a viewport width or a Tailwind breakpoint
  When plan-checker looks for a low-fidelity wireframe or a cited measurement for that option at that width
  Then the scan reports HIGH when neither is present
  And the finding quotes the drop reason and names the missing width
```

```gherkin
Scenario: AC-7 An option dropped on a breakpoint claim backed by an artefact passes
  Given a funnel whose drop reason for an option names a viewport width
  When plan-checker finds a wireframe for that option at that width, or a cited measurement of the rendered result
  Then the scan passes for that clause
```

```gherkin
Scenario: AC-8 The inline-note allowance survives for options carried forward
  Given a funnel option that is carried to the Narrow stage rather than dropped
  When that option's mobile layout is described by an inline note instead of a separate wireframe
  Then the scan passes for that clause
  And the elimination-grade requirement is confirmed to bind drop reasons only
```

### R-C — Prior-Decision Reversal Record

```gherkin
Scenario: AC-9 A plan reversing a predecessor decision without a record is flagged
  Given a plan whose selected design matches an option a named predecessor plan rejected
  When plan-checker finds no Prior-Decision Reversal Record in the plan's tech-docs.md
  Then the scan reports HIGH
  And the finding names the predecessor plan and the reversed decision
```

```gherkin
Scenario: AC-10 A reversal record with a disposition passes
  Given a plan carrying a Prior-Decision Reversal Record in its tech-docs.md
  When plan-checker evaluates the record
  Then the scan passes only if the record names the predecessor plan, the original reason, and one disposition
  And the disposition is one of obsolete, never-measured, wrong-at-the-time, or changed-constraint
```

```gherkin
Scenario: AC-11 A never-measured disposition requires the settling measurement
  Given a Prior-Decision Reversal Record whose disposition is never-measured
  When plan-checker evaluates the record
  Then the scan passes only if the record cites the measurement that settles the original claim
  And a never-measured disposition with no cited measurement is reported as HIGH
```

### R-D — Enumerated-Vocabulary Consistency

```gherkin
Scenario: AC-12 A multi-surface identifier set without a vocabulary record is flagged
  Given a plan introducing a closed set of user-visible identifiers reaching more than one binding surface
  When plan-checker finds no Enumerated-Vocabulary Record in the plan
  Then the scan reports MEDIUM
  And the finding lists the binding surfaces the identifiers reach
```

```gherkin
Scenario: AC-13 A vocabulary whose members follow different naming kinds fails its own record
  Given an Enumerated-Vocabulary Record stating one naming rule and listing every member against it
  When any member is shown not to satisfy the stated rule
  Then the record is reported as MEDIUM
  And the finding names the non-conforming member and the rule it breaks
```

### Enforcement wiring

```gherkin
Scenario: AC-14 plan-maker emits every new section on a UI-bearing plan
  Given plan-maker is authoring a UI-bearing plan
  When it writes the prd.md funnel record
  Then the Justify table carries a marked Primary Job Criterion row
  And plan-maker grills the user whenever the Primary Job Criterion winner differs from the selection
```

```gherkin
Scenario: AC-15 plan-fixer scaffolds each section Step 5o can flag
  Given a plan-checker report containing a Step 5o finding
  When plan-fixer processes that finding
  Then it inserts the named scaffold for that clause into the correct plan document
  And it never invents a Primary Job Criterion value in place of the author's judgment
```

```gherkin
Scenario: AC-16 Step 5o is proven non-vacuous before the phase gate closes
  Given a deliberately non-compliant fixture plan exercising all six Step 5o clauses
  When plan-checker runs against the fixture
  Then every clause produces its expected finding at its stated severity
  And a clause producing no finding blocks the phase gate
```

### Parity, retrofit, and record

```gherkin
Scenario: AC-17 Every governance routing reaches all three repositories
  Given the five Knowledge Capture routings and the four new rules
  When the parity grep table is re-run across ose-public, ose-primer, and ose-private
  Then every cell reports present
  And a single absent cell blocks the propagation phase gate
```

```gherkin
Scenario: AC-18 Every open plan carries a recorded audit verdict
  Given every plan folder under plans/in-progress and plans/backlog in the three repositories
  When the retrofit audit completes
  Then each folder appears in this plan's audit table with a verdict
  And a verdict of compliant, fixed, or exempt-with-reason is required for every row
```

```gherkin
Scenario: AC-19 The post-mortem conforms to the post-mortems convention
  Given the post-mortem document written by this plan
  When it is validated against the Post-Mortems Convention
  Then all mandatory sections are present in the required order
  And the filename follows the incident-date pattern and is listed in the post-mortems index
```

```gherkin
Scenario: AC-20 Platform bindings are regenerated after every agent-definition edit
  Given an edit to any file under .claude/agents or .claude/skills
  When the phase gate runs
  Then npm run generate:bindings has been executed and its output is committed
  And a dirty working tree after a second bindings run blocks the gate
```

## Product scope

**In scope**

- The four rule texts, in their authoritative convention homes.
- `plan-checker` Step 5o with six clauses and fixed severities.
- `plan-maker` emission and grilling changes; `plan-fixer` scaffolds; the
  `plan-creating-project-plans` skill's mirrored statement of the rules.
- A non-compliant fixture proving Step 5o fires, exercised at the Phase 3 gate.
- The five-routing parity backfill into `ose-primer` and `ose-private`.
- The post-mortem document and its index entry.
- A recorded audit verdict and applied fix for every open plan in the three repos.
- Platform-binding regeneration in every repo whose `.claude/` tree changes.

**Out of scope**

- Any change to the AI Model Benchmark feature, its dataset, or its tests.
- Binding R-A and R-B to option tables outside the UI design funnel.
- A deterministic validator in `apps/rhino-cli` or a new CI gate.
- Amending anything under `plans/done/`.
- Changing the funnel's artefact rules (both-tiers, Excalidraw tooling, asset placement).

## Exemption records

Stated explicitly rather than left to inference, per the convention that an exemption must be
written down.

| Gate                                                       | Status         | Reason                                                                                                                       |
| ---------------------------------------------------------- | -------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| UI design funnel (this plan's own `prd.md`)                | Exempt         | This plan adds and changes no user-facing screen or component under `apps/` or `libs/`; it is governance-only                |
| Specs and Gherkin companion `.feature` files               | Exempt         | No runtime behaviour changes; the acceptance criteria above describe agent-prose contracts, which have no step-binding layer |
| Rule 15 three-tester web retest                            | Exempt         | No web UI is changed, so the live-site testers have nothing to exercise                                                      |
| Rule 16 API exploratory retest                             | Exempt         | No REST or GraphQL endpoint is changed                                                                                       |
| Learning-plan `syllabus/` record                           | Exempt         | No course, tutorial, or curriculum content is authored or restructured                                                       |
| Prior-Decision Reversal Record (R-C, applied to this plan) | Not applicable | This plan reverses no predecessor decision; it adds rules that did not previously exist                                      |

## Product-level risks

| Risk                                                                                      | Mitigation                                                                                                                       |
| ----------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| The Primary Job Criterion is written to match whichever option the author already prefers | AC-2 requires a `brd.md` anchor, so the criterion must exist as a stated problem before the options are scored                   |
| Step 5o's pattern-matched clauses (AC-3, AC-12) misfire on legitimate wording             | Both are MEDIUM, not HIGH, and both quote the matched text so a false positive is dismissible in one read                        |
| The retrofit changes plans other people are mid-execution on                              | Retrofit edits are confined to `prd.md` funnel tables and `tech-docs.md` records; no `delivery.md` checkbox state is touched     |
| A fixture proving Step 5o works becomes stale as the clauses evolve                       | The fixture lives with the plan and is exercised at a gate, not committed as a permanent test asset; its role ends at Phase 3    |
| Four rules landing together overwhelm the reader of an already-long convention            | Each rule is a short subsection stating gap, application, and enforcing clause; the long-form reasoning lives in the post-mortem |
