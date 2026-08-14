# Validation Scope 4-5: Delivery Checklist, PR Authorization, Consistency

## 4. Delivery Checklist Validation

Steps executable, sequential, granular; validation/acceptance criteria specific and testable; git
workflow specified. Named HARD RULEs (each validated in full detail by a later numbered rule/step
noted below — this section is the summary layer):

- **TDD-shaped steps**: any code-shipping item needs a test-first step (Red→Green→Refactor). Missing
  failing-test step before implementation: **HIGH**. See
  [Test-Driven Development Convention](../../../../repo-governance/development/workflow/test-driven-development.md).
- **TDD phase separation (HARD RULE)**: RED, GREEN, REFACTOR each their own `- [ ]` checkbox — a
  combined checkbox is **HIGH**. See
  [TDD Shape for Delivery Checklists](../../../../repo-governance/development/workflow/test-driven-development/08-tdd-shape-for-delivery-checklists.md#tdd-shape-for-delivery-checklists).
- **Non-code step format**: non-code steps (docs, config, governance) use
  `[Action verb] [file] — acceptance: [outcome]`, not RED/GREEN/REFACTOR. Misapplied TDD shape:
  **MEDIUM**.
- **Execution-grade clarity (HARD RULE)**: every checkbox names explicit file path(s), verbatim
  shell command(s), and a concrete acceptance criterion — bare "implement X"/"set up Y" is **HIGH**.
  Full detail in `reference/04-operational-readiness-through-worktree.md` rule 11 (Step 5e). See
  [Plans Organization Convention §Execution-Grade Clarity](../../../../repo-governance/conventions/structure/plans/16-execution-grade-clarity.md#execution-grade-clarity-hard-rule).
- **Executor tagging (HARD RULE)**: every checkbox declares `[AI]`/`[HUMAN]`/`[AI+HUMAN]` (unmarked
  = `[AI]`) with a legend at the checklist top; untagged or mis-tagged human-only step: **HIGH**.
  Full detail in `reference/05-anti-hallucination-through-phasegate.md` rule 14 (Step 5h).
- **Phase gate and natural pause (HARD RULE)**: every phase ends with `### Phase N Gate`
  (must-pass checklist plus Pause Safety note) at a safe-to-stop state; missing gate: **HIGH**; a
  merge-worthy non-pause phase: **MEDIUM**. Full detail in
  `reference/05-anti-hallucination-through-phasegate.md` rule 15 (Step 5i).
- **Phase 0 opens no PR (HARD RULE)**: Phase 0 (Environment Setup and Baseline) carries no
  PR-creation, branch-push, PR-Review-Cycle, merge, `gh pr ready`, or post-push CI-verification step
  under any Delivery Mode — earliest PR-opening phase is Phase 1. Flag violations, and any unscoped
  Per-Phase Integration Protocol block, **HIGH**. Full detail below (PR Step Authorization Check) and
  `reference/07-delivery-mode-syllabus-vercel.md` rule 19 item 7. See
  [Plans Organization Convention §Phase 0 Opens No PR](../../../../repo-governance/conventions/structure/plans/23-phase-0-opens-no-pr.md#phase-0-opens-no-pr--the-earliest-pr-is-phase-1-hard-rule).
- **PRs open at delivery boundaries, not every phase (HARD RULE)**: a PR opens at each
  **delivery boundary** — the phase after which accumulated work is independently shippable — not
  once per phase; the contiguous phases ending at a boundary form a **delivery unit** mapping to one
  branch, one PR (the worktree stays a coarser per-repository unit, capped at one per repo per plan
  — see
  [Worktree Cap](../../../../repo-governance/conventions/structure/plans/31-worktree-cap.md#worktree-cap--one-worktree-per-repository-per-plan-hard-rule)).
  Flag **HIGH** an integration step in a non-boundary phase, a change-producing phase absent from
  `### Delivery Boundaries`, or a non-boundary final change-producing phase; flag **MEDIUM** a
  missing `### Delivery Boundaries` table on a non-trivial plan, or a single end-of-plan boundary
  against a `## Parallelization Model` declaring independent parallel nodes. Full detail below and
  `reference/07-delivery-mode-syllabus-vercel.md` rule 19 item 8. See
  [Plans Organization Convention §PRs Open at Delivery Boundaries](../../../../repo-governance/conventions/structure/plans/25-prs-open-at-delivery-boundaries-rules.md#prs-open-at-delivery-boundaries-not-every-phase-hard-rule).
- **Specs and Gherkin delivery (Two Paths)**: a plan changing observable behavior in `apps/`,
  `libs/`, or `specs/` needs delivery steps adding/updating companion `specs/` `.feature` files and
  running `specs:coverage`. Full detail in `reference/06-specs-ui-knowledge-capture.md` rule 16
  (Step 5j). See
  [Feature Change Completeness Convention §Two Paths](../../../../repo-governance/development/quality/feature-change-completeness.md).
- **Gherkin-tagged TDD steps (one scenario per cycle)**: every behavior RED→GREEN→REFACTOR cycle
  targets exactly one Gherkin scenario — RED carries a single-scenario `**Gherkin (binds) →**`
  tag plus the verbatim inline scenario. **HIGH** a multi-scenario `binds` tag, a missing tag, or a
  non-verbatim inline block. Exceptions (keep multi-scenario `;`-lists): pure-core
  `**Gherkin (underpins) →**` unit tests, and aggregate BDD binders consuming a whole `.feature`.
  Pure refactors and docs/governance-only steps exempt. See
  [Gherkin-Tagged Delivery Steps](../../../../repo-governance/development/workflow/test-driven-development/09-gherkin-tagged-delivery-steps.md#gherkin-tagged-delivery-steps).
- **UI-design-funnel completeness (UI-bearing plans)**: plans adding/changing user-facing
  screens/components need the design-funnel artefacts (≥2 named low-fi alternatives, 2 hi-fi
  `.excalidraw.png` finalists, named selection, rationale, grounding/prior-art note, responsive
  strategy across mobile/tablet/desktop). Full detail in
  `reference/06-specs-ui-knowledge-capture.md` rule 17 (Step 5k). Pure-refactor/no-UI/
  governance-only plans exempt. See
  [UI Mockups in Plan Docs convention](../../../../repo-governance/conventions/formatting/diagrams/42-ui-mockups-principles-and-scope.md#ui-mockups-in-plan-docs-principles-in-practice-and-scope).
- **Manual-assertion locale and evidence completeness (UI/API plans)**: manual-assertion steps must
  cover all supported locales on a multi-locale app and capture committed evidence (screenshots to
  `evidence/`, curl responses inlined). Full detail in
  `reference/04-operational-readiness-through-worktree.md` rule 9 items 4-5 (Step 5c). Single-locale
  coverage, or no evidence-capture step, is **HIGH**. See
  [Evidence Capture Convention](../../../../repo-governance/development/quality/evidence-capture.md).
- **Rule-15 three-tester retest (web-UI feature-change plans)**: a near-end step runs the
  [`web-ux-test-fixing-planning`](../../../../repo-governance/workflows/web/web-ux-test-fixing-planning.md)
  triad (`web-exploratory-tester`, `web-usability-tester`, `web-design-tester`) across all supported
  locales, with every EWT/UWT/DWT defect finding folded into `delivery.md` as an unchecked checkbox
  fixed before archival (deferral needs explicit user permission, only when genuinely impossible;
  SG-###/USS-### proposals may be triaged/deferred). Unfixed defect checkbox at archival, missing
  step, or single-locale scope: **HIGH**. CLI/text-output and pure governance/agent-definition plans
  exempt. See
  [User-Facing Delivery Hardening](../../../../repo-governance/development/quality/user-facing-delivery-hardening.md)
  Rule 15.
- **Rule-16 API exploratory retest (API feature-change plans)**: a near-end step runs
  `api-exploratory-tester` (`output-mode: delivery`) against the running endpoint(s), with every
  AET-### defect finding folded into `delivery.md` and fixed before archival (same deferral rule;
  SG-### proposals triageable). Unfixed defect checkbox, or missing step on an API feature-change
  plan: **HIGH**. Independent of Rule 15 (a plan changing both UI and API carries both retests).
  Frontend-only/CLI/governance-only plans exempt. See
  [User-Facing Delivery Hardening](../../../../repo-governance/development/quality/user-facing-delivery-hardening.md)
  Rule 16.
- **Knowledge Capture phase presence**: every substantive plan's `delivery.md` carries a final
  Knowledge Capture phase (or explicit "none" record). Full detail in
  `reference/06-specs-ui-knowledge-capture.md` rule 18 (Step 5l). Silent absence: **MEDIUM**;
  explicit "none": PASS. See
  [Knowledge Capture Convention](../../../../repo-governance/development/quality/knowledge-capture.md).

### Delivery Checklist Granularity Standard

- Each checkbox is a single, independently verifiable action — not a paragraph of actions.
- Multi-action items must split (e.g. "Install X, configure Y, and verify Z" → 3 checkboxes).
- Every item has a clear done-state.
- Phase transitions have explicit verification steps (e.g. "Verify `nx run app:typecheck` passes").
- Maximum nesting depth: 2 levels (top-level checkbox with sub-checkboxes, no deeper).
- Sub-items independently checkable — completing a parent doesn't auto-complete children.

## PR Step Authorization Check

Authoritative source:
[Plans Organization Convention §Delivery Mode](../../../../repo-governance/conventions/structure/plans/32-delivery-mode-the-four-modes.md#delivery-mode).

A PR-creation step is **expected and correct** when the plan's resolved Delivery Mode is
`worktree-to-pr` (default) or `main-to-pr` — validate via rule 19 (Step 5m) instead (PR-Review
Maker→Fixer Cycle present, merge tag correct). Flag **HIGH** a PR-creation step on a plan resolved to
`worktree-to-origin-main` or `main-to-origin-main` (direct-push) — remove the step or correct the
mode. Executing inside a worktree does not by itself select a mode either way — only the resolved
Delivery Mode is the authorizing signal.

**Phase 0 Never Opens a PR — mode-independent (HIGH)**. Authoritative source:
[Plans Organization Convention §Phase 0 Opens No PR](../../../../repo-governance/conventions/structure/plans/23-phase-0-opens-no-pr.md#phase-0-opens-no-pr--the-earliest-pr-is-phase-1-hard-rule).
Flag **HIGH**, regardless of mode, any of the following inside `## Phase 0` (steps, sub-bullets, or
its Gate): a PR-creation step; a branch-push step to any target; a PR-Review Maker→Fixer Cycle step
or completion reference; a merge step, `gh pr ready` step, or post-push CI-verification step. A
`*-to-pr` mode authorizes PR steps only at delivery boundaries — Phase 0 produces nothing reviewable,
so the earliest PR-opening phase is Phase 1, and only if Phase 1 is a declared boundary. Also flag
**HIGH** a Per-Phase Integration Protocol block not scoped to Phase 1 onward.

Remediation: delete the offending step; if Phase 0 wrote evidence artifacts, note they ride the
Phase 1 PR; if Phase 0 genuinely produces reviewable changes, flag it as mis-scoped and move the work
to Phase 1.

**Detection command** (from the plan folder; Phase 0 slice only):

```bash
awk '/^## Phase 0/{f=1} /^## Phase 1/{f=0} f' delivery.md \
  | grep -nEi 'gh pr create|gh pr ready|open (a )?(draft )?pr|create pr|git push|push to origin|PR-Review|review cycle|merge(d)? (the )?PR' \
  | grep -c .
```

Acceptance: returns `0`. Falsifiable both ways: a `gh pr create --draft` line inside Phase 0 makes it
return `1`. Read the printed number (don't `&&`-chain — `grep -c` exits 1 on zero count). Single-file
plan: substitute `README.md`.

## No PR Outside a Declared Delivery Boundary (HIGH)

Flag **HIGH** any PR-creation, PR-Review-Cycle, `gh pr ready`, merge, or post-push CI-verification
step in a phase not declared a boundary in `### Delivery Boundaries`.

**Detection commands** (from the plan folder; compare the two number sets):

```bash
# (1) phases the plan DECLARES as delivery boundaries
grep -oE 'yes[^|]*Phase [0-9]+' delivery.md | grep -oE '[0-9]+$' | sort -un | tr '\n' ' '

# (2) phases that ACTUALLY carry an integration step
awk '
  /^## Phase [0-9]+/ { n=$3; sub(/[^0-9].*$/,"",n) }
  /^ *- \[ \]/       { if (buf) print buf; buf = n "\t" $0; next }
  /^ *- \[x\]/ || /^ *$/ || /^#/ { if (buf) print buf; buf = ""; next }
  buf                { buf = buf " " $0 }
  END                { if (buf) print buf }
' delivery.md \
  | grep -viE 'gh pr list|no PR (here|at this gate)' \
  | grep -Ei 'gh pr create|gh pr ready|open (a )?(draft )?pr|draft pr opened|PR-Review|review cycle|\[AI\]`?-merged|auto-merge' \
  | cut -f1 | sort -un | tr '\n' ' '
```

Command (2) restricts to **unticked** `- [ ]` lines deliberately: _checklist_ excludes prose (a
sentence mentioning "merged PR" isn't a step); _unticked_ excludes history (a `- [x]` step is a merge
that already happened — unactionable, and would fire forever on a part-executed plan). The rule binds
PRs a plan has **yet** to open, not executed history.

The awk accumulates each checklist **item** (its `- [ ]` line plus wrapped continuation lines) before
matching — load-bearing, not tidiness: a boundary step typically reads `- [ ] [AI] **Delivery
boundary …PR opens.**` on one line with `[AI]-merged` on a following indented line. Line-by-line
matching puts the keyword out of reach and silently reports zero integration steps on a plan with
three — the worst failure mode for a checker. The `grep -v` pre-filter drops steps that _query_
integration (e.g. `gh pr list --state open`) rather than cause it.

Sanity-check on a trusted plan before believing a zero. Acceptance: every number in (2) also appears
in (1). Falsifiable both ways: `gh pr create` added to an intermediate phase appears in (2) not (1)
(fails); promoting it to a boundary row makes it appear in both (passes). A number in (1) absent from
(2) is the separate defect of a declared boundary with no integration step — report it too.

Also flag: a change-producing phase in **no** table row (**HIGH** — no declared route to `main`); a
non-boundary final change-producing phase (**HIGH** — that work never merges); a missing
`### Delivery Boundaries` table on a non-trivial plan (**MEDIUM**,
`grep -c '^### Delivery Boundaries' delivery.md` returns `0`); a single end-of-plan boundary against
a `## Parallelization Model` declaring independent parallel nodes (**MEDIUM** — re-serialises the
DAG).

Remediation: move integration steps to the delivery unit's boundary phase, or promote a genuinely
boundary-qualifying intermediate phase and add its table row. Never delete the work's route to
`main`.

## 5. Consistency Validation

Requirements align with delivery steps; technical docs support the implementation approach;
acceptance criteria match user stories; no contradictions between sections.
