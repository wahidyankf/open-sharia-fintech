---
name: web-ux-test-fixing-planning
title: "web-ux-test-fixing-planning"
goal: >
  Run the three live-site UX-quality testers — spec-aware exploratory (correctness), spec-blind
  heuristic-usability, and design-aware design-fidelity — against the same live URL(s) and goal,
  sequentially, integrating each result set into the plan before the next runs, then solidify one
  fix-ready plan whose findings section keeps the three sources clearly separated (exploratory EWT-###
  vs usability UWT-### vs design DWT-###) and which carries a tech-docs.md (root-cause + fix approach),
  a TDD-shaped delivery.md describing how to fix every finding, and — when the plan is UI-bearing — an
  assets/ folder of both-tier (lo-fi + hi-fi) UI mockups. The deliverable is the plan, never the fixes.
termination: >
  A grill-validated plan exists under plans/in-progress/<identifier>/ containing README.md, brd.md,
  prd.md, findings.md (with separate Exploratory, Usability, and Design sections), tech-docs.md, and
  delivery.md, passes plan-quality-gate at strict mode, and is pushed to the requested git target.
  No application or library source under apps/ or libs/ is modified by this workflow.
inputs:
  - name: target-urls
    type: string
    description: >
      One or more live URLs to test (comma-separated). The same set is handed to all three testers so
      the exploratory, usability, and design passes judge identical surfaces. The running dev/preview
      server must already be reachable (HTTP 200) before the workflow starts.
    required: true
  - name: testing-goal
    type: string
    description: >
      The shared charter/goal forwarded verbatim to all three testers (e.g. "thoroughly test the
      cost-of-living calculator tool page"). Each tester interprets it through its own lens —
      exploratory hunts correctness/spec defects, usability judges first-time-user friction, design
      judges live mockup/token/design-system fidelity and design practice.
    required: true
  - name: plan-mode
    type: enum
    values: [new, merge]
    description: >
      Whether to create a brand-new plan (default) or merge the combined findings into an existing
      plan folder. "merge" requires target-plan-path.
    required: false
    default: new
  - name: plan-identifier
    type: string
    description: >
      Slug for the new plan folder under plans/in-progress/ (no date prefix per Plans convention).
      Default is derived from the target (e.g. "<app>-<feature>-test-fixing"). Ignored when
      plan-mode=merge.
    required: false
  - name: target-plan-path
    type: string
    description: >
      When plan-mode=merge, the existing plan folder under plans/in-progress/ to merge the combined
      findings into. Required when plan-mode=merge; ignored otherwise.
    required: false
  - name: breakpoints
    type: string
    description: >
      Optional comma-separated viewport widths (px) to exercise responsive behaviour. Forwarded to
      all three testers. Default is the testers' own standard set (e.g. 320, 375, 768, 1024, 1280, 1440).
    required: false
  - name: locales
    type: string
    description: >
      Optional comma-separated locale path segments to cover (e.g. "en, id"). Forwarded to all three
      testers. Default and minimum is ALL locales the target supports (discovered from the app's i18n
      config or the locale-prefixed routes) — not just the default locale. Testing only one locale on
      a multi-locale app is incomplete.
    required: false
  - name: mode
    type: enum
    values: [lax, normal, strict, ocd]
    description: "Quality threshold for the nested plan-quality-gate. Default: strict."
    required: false
    default: strict
  - name: max-concurrency
    type: number
    description: >
      Maximum agents run in parallel. Default 1: the three testers run SEQUENTIALLY by design
      (exploratory → integrate → usability → integrate → design → integrate) so each result set is
      folded into the plan before the next runs, and because all three testers are sonnet-tier the
      staged order keeps each pass's full context available during its integration.
      This 1 is a genuine DAG serialization point, NOT a stale concurrency cap: each tester
      reads the plan the previous tester wrote, so the nodes are dependent by the standard
      independence test (two nodes are independent only when neither reads what the other
      writes). The DAG governs — never force parallelism onto dependent nodes. Raising this to
      the N+1 model's default N would produce three testers racing on one plan file, which is
      why this workflow is deliberately exempt from that default.
    required: false
    default: 1
  - name: push-target
    type: string
    description: "Git push destination for the finished plan. Default: origin main."
    required: false
    default: "origin main"
outputs:
  - name: plan-path
    type: string
    description: Path to the created or updated plan under plans/in-progress/<identifier>/
  - name: exploratory-findings-count
    type: number
    description: Number of EWT-### findings carried into the combined plan
  - name: usability-findings-count
    type: number
    description: Number of UWT-### findings carried into the combined plan
  - name: design-findings-count
    type: number
    description: Number of DWT-### findings carried into the combined plan
  - name: final-status
    type: enum
    values: [pass, partial, fail]
    description: Final status after the plan's quality gate
---

# Web UX Test-Fixing Planning Workflow

**Purpose**: Test a live website from the three complementary live-site UX-quality lenses in one pass —
spec-aware exploratory correctness (`web-exploratory-tester`), spec-blind heuristic-usability
(`web-usability-tester`), and design-aware design-fidelity (`web-design-tester`) — then fold all three
result sets into a single fix-ready plan whose findings stay attributed to their source and which
spells out, in `tech-docs.md` and a TDD-shaped `delivery.md`, exactly how to fix what was found.

> **The outcome is the plan, not the implementation.** This workflow never edits app/lib source,
> never runs a fix, and never lands behaviour changes. It produces a proposal under
> `plans/in-progress/`. The actual fixes happen later, only after a human reviews the plan and runs
> the [Plan Execution workflow](../plan/plan-execution.md). `delivery.md` becomes the executable
> checklist then, not now.

This is a `planning`-type workflow: a single forward procedure whose terminal deliverable is a plan
document. It is **not** an iterative quality gate over the site.

## Execution Mode

**Agent Delegation (preferred)** — the calling context orchestrates the phases, delegating the three
testing passes to `web-exploratory-tester`, `web-usability-tester`, and `web-design-tester` via the
Agent tool **one at a time** (exploratory → integrate → usability → integrate → design → integrate),
running the solidification and plan authoring through `plan-maker`, and gating with `plan-checker` /
`plan-fixer`. The human grill checkpoint runs inline so the user's conversation is preserved.

**Manual Orchestration (fallback)** — when those agents are unavailable as delegated agent types,
the assistant executes each phase directly using the testers' and plan agents' documented procedures
with Read/Write/Edit tools.

## When to use

- You have a running site (dev, preview, or production) and want a correctness sweep, a first-time-user
  usability read, and a design-fidelity check, delivered as one actionable fix plan rather than three
  disconnected reports.
- Before hardening a user-facing feature: capture defects, friction, and design drift together so the
  fix plan addresses all three in one delivery checklist. This is the near-end three-tester round that
  web-UI feature-change plans must run per
  [User-Facing Delivery Hardening](../../development/quality/user-facing-delivery-hardening.md) (Rule 15).
- To refresh an existing findings plan: re-run all three testers and merge the new results into the
  prior plan folder (`plan-mode=merge`).

> **Output-mode note**: This workflow invokes the testers in their default **`plan` output-mode** —
> each tester files its findings into the new (or merged) plan folder that this workflow consolidates.
> The **`delivery` output-mode** is the in-place rule-15 variant used when findings belong to a plan
> already in flight: invoke each tester directly with `output-mode: delivery` and the executing
> plan's `plan-path` (see the
> [Rule-15 three-tester retest in plan-execution](../plan/plan-execution.md#8-finalization-and-archival-sequential)).
> This workflow's behavior is unchanged; the note clarifies which mode each path uses.

## Inputs at a glance

| Input              | Required | Default               | Notes                                      |
| ------------------ | -------- | --------------------- | ------------------------------------------ |
| `target-urls`      | yes      | —                     | Same set handed to all three testers       |
| `testing-goal`     | yes      | —                     | Shared charter, interpreted per lens       |
| `plan-mode`        | no       | `new`                 | `new` creates a plan; `merge` updates one  |
| `plan-identifier`  | no       | derived from target   | New-plan slug (no date prefix)             |
| `target-plan-path` | no       | —                     | Required when `plan-mode=merge`            |
| `breakpoints`      | no       | testers' standard set | Responsive viewports                       |
| `locales`          | no       | ALL supported locales | Locale path segments (never default-only)  |
| `mode`             | no       | `strict`              | Threshold for the nested plan-quality-gate |
| `push-target`      | no       | `origin main`         | Git destination for the finished plan      |

## Grilling (Human Checkpoints)

This workflow **grills the user hard whenever a decision is genuinely needed** — it never guesses a
material choice. Every grill question is asked with the `AskUserQuestion` tool as a multiple-choice
prompt per the
[Grilling-With-Options Convention](../../development/workflow/grilling-with-options.md), and every
question always offers the standing options required by that convention (a blank-state / "none of
these" type answer **and** a "let's chat about this" escape hatch). Grill only when the answer
changes what the workflow does; when a sensible default exists, take it and state it.

Decision points that trigger a grill:

- **Pre-flight** — ambiguous or multi-candidate target URLs; `plan-mode` (new vs merge) when not
  given; the new-plan `plan-identifier`; which `locales`/`breakpoints` to cover when the target is
  multi-locale or the responsive scope is unclear.
- **After all three passes are integrated (entering Phase 4)** — which findings are in scope vs
  deferred; prioritization/severity disputes; the **fix approach** where more than one valid option
  exists; whether to accept each `SG-###` (exploratory or design) as a specs addition.
- **UI direction (UI-bearing plans)** — which low-fidelity alternative advances to high-fidelity, and
  which high-fidelity finalist is selected (the design-funnel decision), grilled before the
  `.excalidraw.png` finalists are committed.
- **Before push** — confirm the `push-target` when it differs from the default.

The Phase 4 `plan-maker` invocation performs its own before/after grill as part of authoring; this
section governs the workflow-level checkpoints around it so no material decision is made silently.

## Systematic Coverage & Recurrence (all three testers)

A standing finding from re-running this workflow on the same target: dimension- and charter-driven
testing reliably surfaces _representative_ defects yet repeatedly misses the **"enumerate every element
and assert one property"** class — a shared control that no-ops on one tab, an input whose state never
reaches the URL, a stated invariant only half-implemented, a raw unstyled control, a hidden affordance,
a jargon label, a redundantly duplicated panel. The three testers now each carry **mandatory
forcing-function sweeps** for these (see each tester's _Mandatory Systematic Sweeps/Probes/Checks_
section). This workflow adds three cross-tester obligations on top:

- **Coverage-matrix artifact** — each tester records its enumerated matrices (control × surface,
  control × URL-round-trip, element × styling, declared-invariant conformance) in its coverage map; the
  consolidated plan's `README.md` keeps them so a reviewer can see _what was enumerated_, not just _what
  was found_. A sampled or empty matrix is not coverage.
- **Recurrence re-check** — the prior-class list compiled in Phase 0 is handed to every tester as a
  mandatory re-check, so a target does not keep re-yielding a class a fresh charter would skip.
- **Changed-surface targeting** — the diff-since-last-run list from Phase 0 directs explicit coverage of
  features added/changed after the previous test (the highest-risk untested surface).

These obligations are passed to each tester as part of its Phase 1–3 args and verified by the
cross-tester completeness critic in Phase 3.5.

## Phases

### 0. Pre-flight (Sequential)

**Actions**:

- Confirm the `ose-public` working tree is clean (`git status --porcelain` empty).
- Verify every URL in `target-urls` returns HTTP 200 (curl). If the server is down, abort and ask
  the user to start it — the testers cannot run against a dead target.
- Resolve `plan-mode`. For `new`, resolve `plan-identifier` (input, else derive from the target,
  e.g. `ayokoding-www-calc-test-fixing`). For `merge`, require `target-plan-path` to point at an
  existing folder under `plans/in-progress/`; abort if absent.
- Resolve `breakpoints` and `locales` (defaults = testers' own standard coverage; `locales` defaults
  to ALL locales the target supports — discovered from the app's i18n config or locale-prefixed
  routes — never just the default locale).
- **Recurrence memory** — locate prior findings plans for this target (`plans/**` whose slug names the
  same app/feature) and extract the **classes** of defect they recorded (e.g. cross-tab consistency,
  state-not-in-URL, unstyled control, hidden affordance). Hand this class list to all three testers as a
  **mandatory re-check** so a target does not keep re-yielding the same class a fresh charter would skip.
- **Diff-since-last-run targeting** — determine what changed in the target's source since the last
  findings run (`git log`/`git diff` on `apps/<target>/**`, `libs/**`). Features added or changed after
  the prior test are the **highest-risk untested surface**; direct the testers to cover them explicitly.

**Output**: Targets reachable; plan destination resolved; prior-class re-check list + changed-surface
list compiled for the testers.

**On failure**: Dirty tree → ask the user to commit/stash first. Unreachable URL or missing
merge target → abort with a clear message.

### 1. Exploratory Pass + Integrate (Sequential, delegated)

Run the spec-aware tester **first, alone**, then fold its results into the plan before the usability
pass starts. It is **non-destructive / passive** — it reads, clicks, resizes, and probes but never
mutates server state.

**Agent**: `web-exploratory-tester` — spec-aware. Compares live behaviour against existing
`specs/**` Gherkin; actively hunts edge cases and boundary conditions; produces a findings catalog
`EWT-###` (functional, behavioural-consistency, edge-case/boundary, UI/UX, responsive, accessibility,
URL/IA, passive security) plus spec-gap proposals `SG-###` (Gherkin scenarios for correct-but-unspecced
behaviour, edge cases especially).

- **Args**: `target-urls: {input.target-urls}`, `testing-goal: {input.testing-goal}`,
  `breakpoints: {input.breakpoints}`, `locales: {input.locales}`, plus the Phase 0 **recurrence
  re-check list** (prior-finding classes for this target) and **changed-surface list** (source changed
  since the last run) as mandatory coverage, and the instruction to record its enumerated coverage
  matrices in the coverage map.
- **Output**: Returns its full findings set as structured text (README/brd/prd/findings/spec-gaps
  bodies). Subagents cannot write under `plans/` directly, so the orchestrator captures the returned
  text.

**Integrate**: Establish the plan skeleton under `plan-path` (or, for `plan-mode=merge`, open the
existing folder) and write the Exploratory half: a `## Exploratory findings (EWT-###)` section in
`findings.md`, the `spec-gaps.md` proposals, and the exploratory slice of README/brd/prd. Preserve
the tester's original IDs.

**Success criteria**: Exploratory findings (possibly empty) integrated into the plan.
**On failure**: If the tester fails, record the gap prominently in the plan README and proceed to
Phase 2 with the usability and design perspectives — never silently drop a perspective.

### 2. Usability Pass + Integrate (Sequential, delegated)

Only after Phase 1 has integrated, run the spec-blind tester and fold its results into the **same**
plan. Also passive / non-destructive.

**Agent**: `web-usability-tester` — spec-blind. Deliberately ignores specs/source/mockups; judges
only first-time-user perception against Nielsen's 10 heuristics (0–4 severity), cognitive walkthrough,
information scent, edge-case UX states (empty/zero-result/loading/error), and responsive usability;
produces a findings catalog `UWT-###`. Emits no spec-_gaps_ (gap analysis requires reading the specs,
which it refuses), but MAY emit `USS-###` **spec-suggestions** — Gherkin scenarios for behaviour a
first-timer expects but the page lacks, each flagged as a spec-blind candidate for reconciliation.

- **Args**: same as Phase 1.
- **Output**: Returns its findings + `walkthrough` + any `USS-###` spec-suggestions as structured text.

**Integrate**: Add a **separate** `## Usability findings (UWT-###)` section to `findings.md` and the
`walkthrough.md` transcript, merge the usability slice into README/brd/prd, and add a short
**cross-reference note** flagging where an EWT and a UWT describe the same underlying defect (e.g. the
`html lang="en"` locale issue both will catch) so the shared root cause is fixed once. The findings
of the two sources MUST remain in their own labelled sections — a reader must always be able to tell
an exploratory finding from a usability finding. Carry the usability tester's `USS-###`
**spec-suggestions** into the plan's spec coverage too — keep them labelled as spec-blind suggestions
distinct from the exploratory `SG-###` spec-gaps, and let the Phase 4 grill decide which to accept into
`specs/**`.

**Success criteria**: Both findings sections present and source-attributed in one `findings.md`;
`SG-###` and `USS-###` spec proposals captured and kept distinct.

### 3. Design Pass + Integrate (Sequential, delegated)

Only after Phase 2 has integrated, run the design-aware tester and fold its results into the **same**
plan. Also passive / non-destructive.

**Agent**: `web-design-tester` — design-aware. Judges whether the **running** rendered page matches its
design and follows good design practice, against five ground-truth sources (committed plan-folder
mockups, design tokens/theme at runtime, design-system primitives `libs/web-ui`, an optional external
Figma/mockup source passed at invocation, and general design best-practice grounded by
`web-researcher`); produces a findings catalog `DWT-###` (mockup fidelity, runtime token/theme fidelity,
design-system-primitive reuse, visual hierarchy, alignment, spacing/density "not cramped", typography,
colour, cross-surface visual consistency) plus design-spec proposals `SG-###` (Gherkin for on-design
behaviours worth protecting). It is the **runtime** counterpart to `swe-ui-checker`'s **static** source
audit and never audits component source.

- **Args**: same as Phase 1, plus an optional `design-source` (Figma link / mockup URL) when one is
  provided.
- **Output**: Returns its findings (README/brd/prd/findings/spec-gaps bodies) as structured text.

**Integrate**: Add a **separate** `## Design findings (DWT-###)` section to `findings.md`, merge the
design slice into README/brd/prd, and extend the cross-reference note flagging where an EWT, a UWT, and
a DWT describe the same underlying defect (e.g. a responsive issue all three touch) so the shared root
cause is fixed once. The three sources MUST remain in their own labelled sections — a reader must always
be able to tell an exploratory finding from a usability finding from a design finding. Carry the design
tester's `SG-###` design-spec proposals into the plan's spec coverage, kept distinct from the usability
`USS-###` suggestions.

**Success criteria**: All three findings sections present and source-attributed in one `findings.md`;
design `SG-###` proposals captured.
**On failure**: If the tester fails, record the gap prominently in the plan README and proceed to
solidification with the exploratory + usability perspectives — never silently drop a perspective.

### 3.5 Cross-tester completeness critic (Sequential)

Before solidifying, run one explicit critic pass over the three integrated result sets and their
coverage matrices, asking: **"which control, surface, tab, locale, breakpoint, edge state, declared
invariant, or recurrence-class did NONE of the three testers enumerate?"** Concretely:

- Reconcile the three coverage maps into a single control × surface grid; any cell no tester exercised
  is either filled by a targeted re-run of the relevant tester or recorded under "areas not covered"
  with the reason.
- Confirm every prior-class re-check item (Phase 0 recurrence list) and every changed-surface item
  (Phase 0 diff list) was actually exercised; re-dispatch the owning tester for any that slipped.
- Confirm the declared-invariant conformance pass enumerated **every** applicable element, not a sample.

Silent omission reads as "all clear" when it is not — this critic makes the gaps explicit before the
plan is authored. Record its outcome in the plan `README.md` coverage map.

**Success criteria**: every matrix cell is exercised or explicitly recorded as not-covered with a reason;
no Phase 0 recurrence/diff item is silently dropped.

### 4. Solidify — tech-docs, delivery, and (conditional) UI assets (Sequential, delegated)

With both findings sets integrated, solidify the plan into a fix-ready deliverable.

**Agent**: `plan-maker` — grills the user (multiple-choice, per the
[Grilling-With-Options Convention](../../development/workflow/grilling-with-options.md)) on scope,
prioritization, fix approach, and any UI direction, then authors:

- `tech-docs.md` — root-cause analysis and the chosen fix approach per finding (or per finding
  cluster), naming the affected files/components and the design-system primitives involved.
- `delivery.md` — TDD-shaped delivery checklist (RED/GREEN/REFACTOR per code item, file path +
  verbatim command + acceptance criterion), tagged `[AI]`/`[HUMAN]`, with Phase 0 first and the
  **Specs & Gherkin completeness** coverage steps that fold the exploratory `SG-###` proposals into
  `specs/**` Gherkin (per [feature-change-completeness](../../development/quality/feature-change-completeness.md)).
  For a web-UI feature-change plan, the checklist also ends with a **"Rule-15 three-tester retest
  follow-ups"** section: run the three live-site testers (`web-exploratory-tester`,
  `web-usability-tester`, `web-design-tester` — i.e. this `web-ux-test-fixing-planning` round) against
  the running target URL(s) across all locales after the fixes land and the visual sign-off is
  recorded, append each finding as a **new unchecked task-list checkbox** (source-attributed
  `EWT-###`/`UWT-###`/`DWT-###`), and fix/tick each before archival — per the
  [User-Facing Delivery Hardening Convention](../../development/quality/user-facing-delivery-hardening.md)
  (Rule 15).
- Finalize `README.md` so its risk summary labels each top risk `[Exploratory]`, `[Usability]`, or `[Design]`,
  and the document map lists every file including (when present) the `assets/` folder.

**Conditional — UI-bearing gate**: if **any** finding's fix adds or changes a user-facing screen or
component under `apps/`/`libs/`, the plan is **UI-bearing** and MUST carry an `assets/` folder with
the both-tiers mockups required by the
[UI Mockups in Plan Docs convention](../../conventions/formatting/diagrams.md#ui-mockups-in-plan-docs),
exactly as the originating
[salary-savings-calculator plan](../../../plans/done/2026-06-19__ayokoding-www-salary-savings-calculator/assets)
does:

- **Tier 1 (low-fidelity)** — ASCII/Unicode wireframes inline, plus a `ui-<screen>-low-fi-alternatives.md`
  capturing the design-funnel divergence for each changed screen.
- **Tier 2 (high-fidelity)** — `assets/ui-<screen>-option-<x>-<name>.excalidraw.png` for the
  finalists, referenced from `tech-docs.md`/`delivery.md` via `./assets/...png` with descriptive alt
  text. Mobile, tablet, and desktop are all designed (mobile-first); a desktop-only mockup fails.
- **Grounding (R5)** — build every mockup from the existing `libs/web-ui` kit, the target app's
  shell/theme/i18n, and sibling screens; name any net-new component explicitly. Mockup colors use
  design-system tokens (`bg-primary`, `text-destructive`), never raw hex.

If **no** finding touches UI, the plan is non-UI and the `assets/` folder is omitted (the
convention's exemption for non-UI plans applies).

**plan-mode handling**:

- **new**: the full document set lands at `plans/in-progress/<plan-identifier>/`.
- **merge**: new findings are appended to `target-plan-path` by ID continuation (never renumber prior
  findings); prior findings are re-verified as STILL-PRESENT / FIXED with the result recorded; then
  `tech-docs.md`, `delivery.md`, and any `assets/` mockups are extended to cover the new findings.

**Output**: Complete plan document set under `plan-path`; `exploratory-findings-count`,
`usability-findings-count`, and `design-findings-count` tallied.

### 5. Plan Quality Gate (Nested Workflow)

**Workflow**: `plan/plan-quality-gate`

- **Args**: `scope: {plan-path}, mode: {input.mode}`
- **Output**: `{final-status}`

Iterates `plan-checker` → `plan-fixer` to double-zero at the requested mode, confirming the plan's
requirements completeness, technical clarity, and delivery-checklist executability (including the
TDD shape and specs-coverage steps).

**Success criteria**: `plan-quality-gate` returns `pass`.
**On failure**: If it returns `partial` after max-iterations, surface the residual findings to the
user before pushing.

### 6. Push & Hand-back (Sequential)

- Stage the explicit plan paths and the workflow/governance edits only (never `git add -A`; sibling
  repos carry unrelated WIP). Commit with a Conventional Commit message and push to `push-target`.
- Emit a user-visible summary: `plan-path`, `exploratory-findings-count`, `usability-findings-count`,
  `design-findings-count`, `final-status`, and a reminder that the plan is a **snapshot of the site as
  tested** — re-run all three testers if the site changes materially before the plan is executed.

**Output**: `plan-path`, `final-status`, pushed commit.

## Gherkin Success Criteria

```gherkin
Feature: web UX test-fixing planning

Scenario: One run produces one combined, source-attributed plan
  Given a reachable live URL and a testing goal
  And the ose-public working tree is clean
  When the workflow runs to completion in plan-mode=new
  Then a plan exists at plans/in-progress/<identifier>/
  And the plan contains README.md, brd.md, prd.md, findings.md, tech-docs.md, and delivery.md
  And findings.md has separate "Exploratory findings (EWT-###)", "Usability findings (UWT-###)", and "Design findings (DWT-###)" sections
  And delivery.md is TDD-shaped with Specs & Gherkin coverage steps
  And the plan passes plan-quality-gate at strict mode
  And no file under apps/ or libs/ source is modified

Scenario: Testers run sequentially with incremental integration
  Given a reachable live URL and a testing goal
  When the workflow runs
  Then the exploratory tester runs and its EWT-### findings are integrated into the plan
  And only then does the usability tester run and its UWT-### findings get integrated
  And only then does the design tester run and its DWT-### findings get integrated
  And tech-docs.md and delivery.md are authored after all three findings sets are integrated

Scenario: A UI-bearing plan carries an assets folder with both-tier mockups
  Given at least one finding's fix changes a user-facing screen or component
  When the plan is solidified
  Then the plan contains an assets/ folder
  And each changed screen has a low-fidelity ASCII wireframe and a high-fidelity .excalidraw.png finalist
  And mobile, tablet, and desktop layouts are all designed
  And mockup colors use design-system tokens rather than raw hex

Scenario: A non-UI plan omits the assets folder
  Given no finding's fix touches a user-facing screen or component
  When the plan is solidified
  Then no assets/ folder is created

Scenario: Merge mode extends an existing findings plan
  Given an existing plan folder under plans/in-progress/
  When the workflow runs in plan-mode=merge against that folder
  Then prior findings keep their original IDs and gain a re-verification result
  And new findings are appended by ID continuation
  And tech-docs.md and delivery.md are extended to cover the new findings

Scenario: Material decisions are grilled with options
  Given more than one valid fix approach exists for a finding
  When the plan is being solidified
  Then the workflow grills the user with a multiple-choice AskUserQuestion
  And the question offers a blank-state option and a "let's chat about this" option
  And no material decision is made without the user's answer

Scenario: Unreachable target aborts before testing
  Given a target URL that does not return HTTP 200
  When the workflow starts
  Then it aborts in pre-flight with a message to start the server
  And no plan is authored

Scenario: Systematic coverage matrices and recurrence are enforced
  Given a target that has prior findings plans and source changed since the last run
  When the workflow runs
  Then pre-flight compiles a prior-finding-class re-check list and a changed-surface list
  And each tester receives them as mandatory coverage and records its enumerated coverage matrices
  And the Phase 3.5 cross-tester completeness critic confirms no matrix cell, recurrence class, or changed surface was silently skipped
  And the consolidated README coverage map carries the matrices
```

## Related Documents

- [web-exploratory-tester Agent](../../../.claude/agents/web-exploratory-tester.md) — Phase 1 spec-aware pass.
- [web-usability-tester Agent](../../../.claude/agents/web-usability-tester.md) — Phase 2 spec-blind pass.
- [web-design-tester Agent](../../../.claude/agents/web-design-tester.md) — Phase 3 design-aware pass.
- [plan-maker Agent](../../../.claude/agents/plan-maker.md) — Phase 4 solidification + tech-docs/delivery/UI-assets authoring.
- [Plan Quality Gate workflow](../plan/plan-quality-gate.md) — Phase 4 nested gate.
- [Plan Execution workflow](../plan/plan-execution.md) — runs the plan later, after human review.
- [UI Mockups in Plan Docs](../../conventions/formatting/diagrams.md#ui-mockups-in-plan-docs) — the both-tiers `assets/` mockup rule a UI-bearing plan must honour.
- [Feature Change Completeness](../../development/quality/feature-change-completeness.md) — the specs+Gherkin rule the delivery checklist must honour.
- [Plans Organization Convention](../../conventions/structure/plans.md) — in-progress plans use the date-free `<identifier>/` folder form.

## Principles Implemented/Respected

- **[Deliberate Problem-Solving](../../principles/general/deliberate-problem-solving.md)**: Three independent perspectives are gathered and reconciled before any fix is proposed; the plan-maker grill forces explicit scope decisions.
- **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)**: Findings stay attributed to their source (EWT vs UWT vs DWT); the fix approach and delivery steps are written down before execution.
- **[Simplicity Over Complexity](../../principles/general/simplicity-over-complexity.md)**: One plan, one delivery checklist — shared root causes are fixed once via the cross-reference note.
- **[Automation Over Manual](../../principles/software-engineering/automation-over-manual.md)**: Testing and authoring are delegated to specialized agents; the gate iterates automatically.
- **[No Time Estimates](../../principles/content/no-time-estimates.md)**: Outcomes, not durations.

## Conventions Implemented/Respected

- **[Live-Tester Systematic Coverage](../../development/quality/live-tester-systematic-coverage.md)**: the cross-tester forcing-functions (enumerate-don't-sample matrices, declared-invariant conformance), the recurrence + diff-since-last-run memory, and the cross-tester completeness critic this workflow enforces are defined canonically here.
- **[Workflow Naming Convention](../../conventions/structure/workflow-naming.md)**: Basename `web-ux-test-fixing-planning` parses as scope=`web`, qualifier=`ux` (the umbrella for the three live-site UX-quality lenses — exploratory correctness, usability, and design), descriptor=`test-fixing`, type=`planning`.
- **[Plans Organization Convention](../../conventions/structure/plans.md)**: The plan lands at `plans/in-progress/<identifier>/` with no date prefix.
- **[Feature Change Completeness](../../development/quality/feature-change-completeness.md)**: The delivery checklist carries the specs+Gherkin coverage steps for the exploratory spec-gap proposals.
- **[UI Mockups in Plan Docs](../../conventions/formatting/diagrams.md#ui-mockups-in-plan-docs)**: A UI-bearing plan carries an `assets/` folder with both-tier (lo-fi ASCII + hi-fi `.excalidraw.png`) mobile/tablet/desktop mockups, design-funnel alternatives, grounding rule, and token-only colors.
- **[Grilling-With-Options Convention](../../development/workflow/grilling-with-options.md)**: Every material decision is grilled via `AskUserQuestion` with multiple-choice options plus the standing blank-state and "chat about this" options.
- **[Subagent Orchestration Convention](../../development/agents/subagent-orchestration.md)**: The three testers run sequentially (one at a time), well within the concurrency cap.
- **[Linking Convention](../../conventions/formatting/linking.md)**: Cross-references use GitHub-compatible markdown links with `.md` extensions.
