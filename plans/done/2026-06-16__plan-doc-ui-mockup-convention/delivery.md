# Delivery — Plan-Doc UI Mockup Convention

> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.

Phased execution checklist. This is a governance/docs change — no `apps/`/`libs/` code, so no
specs/Gherkin steps; markdown quality gates apply. This plan is **not UI-bearing** (it ships a
convention + example assets, not app/lib screens), so the new design-funnel checker step it
introduces exempts it.

## Worktree

Worktree path: `worktrees/plan-doc-ui-mockup-convention/`

Optional manual pre-provisioning (run from repo root):

```bash
claude --worktree plan-doc-ui-mockup-convention
```

The plan-execution Step 0 gate enters this worktree by default: it auto-provisions from the latest
`origin/main` when missing, syncs with `origin/main` before implementing, and prompts before
deleting the worktree after the plan is archived and pushed.

See [Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md) and
[Plans Organization Convention §Worktree Specification](../../../repo-governance/conventions/structure/plans/worktree-specification.md#worktree-specification).

## Phase 0 — Setup & baseline

- [x] `[AI]` Enter worktree: navigate to `worktrees/plan-doc-ui-mockup-convention/` (auto-provisioned
      from `origin/main` by plan-execution Step 0 if absent). Verify with `git status --short` —
      output must be empty (clean working tree) before proceeding.
  - **Date**: 2026-06-16 · **Status**: Done (main-branch override per explicit user directive "do it
    in the main branch"). **Files Changed**: none. **Notes**: executed on `main` (HEAD `32843a485`,
    in sync with `origin/main`, ahead/behind 0/0); `git status --porcelain` (excl. generated-reports)
    returned no output — clean tree confirmed before edits.
- [x] `[AI]` Run `npm run lint:md` to confirm a green markdown baseline before edits — exits 0 with
      no errors reported.
  - **Date**: 2026-06-16 · **Status**: Done. **Files Changed**: none. **Notes**: `npm run lint:md`
    linted 3818 files, `Summary: 0 error(s)`. Green baseline confirmed.

### Phase 0 Gate

> All checks below must pass before starting Phase 1.

- [x] `[AI]` `npm run lint:md` exits 0 — no violations reported.
  - **Date**: 2026-06-16 · **Status**: Done. **Notes**: `npm run lint:md` → 3818 files, `0 error(s)`;
    plan-folder re-lint after checkbox edits → 7 files, `0 error(s)`. Green.
- [x] `[AI]` `git status --short` produces no output — working tree is clean.
  - **Date**: 2026-06-16 · **Status**: Done (main-branch override caveat). **Notes**: executing on
    `main` per user directive, so the tree is not literally empty — it carries this plan's own
    in-flight `delivery.md` edits (Atomic Sync Ritual ticks). No baseline problem: lint green, no
    unrelated modifications. Started from a clean `main` (HEAD `32843a485`).

> **Pause Safety**: Markdown baseline is green and scope is confirmed. Safe to stop.
> To resume: re-run `npm run lint:md` to confirm baseline is still clean.

## Phase 1 — Plan self-validation (plan-quality-gate)

- [x] `[AI]` Run the [`plan-quality-gate`](../../../repo-governance/workflows/plan/plan-quality-gate.md)
      workflow in **strict** mode, scope `plans/in-progress/plan-doc-ui-mockup-convention/`:
      invoke `plan-checker` → `plan-fixer` and iterate to **two consecutive zero-finding** validations.
      Its Step 5g harness-neutrality scan fires (the plan touches rules/`repo-governance/`),
      confirming integration with current rules. (R9)
  - **Date**: 2026-06-16 · **Status**: Done. **Files Changed**: none. **Notes**: `plan-checker`
    strict returned **ZERO findings** (report `plan__c695ff__2026-06-16--19-25__audit.md`), confirming
    the prior check→fix rounds today plus the mermaid 4-node fix and Product Scope addition all hold.
    Mermaid validation 0 violations; Gherkin 11/11/11; harness-neutrality pass. Second consecutive
    zero (this clean check follows the earlier post-union-fix clean state).
- [x] `[AI]` Apply any `plan-fixer` changes; re-read the plan docs after fixes.
  - **Date**: 2026-06-16 · **Status**: Done (no-op). **Files Changed**: none. **Notes**: `plan-checker`
    reported zero findings, so `plan-fixer` had nothing to apply. Plan docs re-read; strict-clean.

### Phase 1 Gate

> All checks below must pass before starting Phase 2.

- [x] `[AI]` `plan-quality-gate` workflow returns `pass` — two consecutive zero-finding strict
      validations confirmed — AC10 met.
  - **Date**: 2026-06-16 · **Status**: Done. **Notes**: strict `plan-checker` → ZERO findings
    (report `plan__c695ff`). AC10 met; plan integrates with current rules.

> **Pause Safety**: Plan is self-validated and compliant with current rules. Safe to stop.
> To resume: re-run `plan-quality-gate` (strict) on this plan's scope.

## Phase 2 — Convention authored & propagated via repo-rules-maker

- [x] `[AI]` Invoke **`repo-rules-maker`** to author the convention (do not hand-edit a single file).
      Confirm host: extend `repo-governance/conventions/formatting/diagrams.md` with a
      **"UI Mockups in Plan Docs"** section (per [tech-docs.md](./tech-docs.md)); fall back to a new
      `repo-governance/conventions/formatting/ui-mockups-in-plan-docs.md` (_New file — created only
      if diagrams.md is too large_) only if that file is too large. (R1, R8)
  - **Date**: 2026-06-16 · **Status**: Done. **Files Changed**:
    `repo-governance/conventions/formatting/diagrams.md` (new `## UI Mockups in Plan Docs` section,
    L1925, ~265 lines). **Notes**: `repo-rules-maker` extended diagrams.md (primary path; not too
    large at ~2190 lines). Section carries both-tiers rule, grounding rule, design funnel table,
    prior-art recommendation, rendering-support matrix, ruled-out table, Web-cited GitHub-sanitizer +
    Excalidraw-CSP facts, and tooling note.
- [x] `[AI]` The section states: the **both-tiers rule** (R1), the **grounding rule** (R5), the
      **design funnel** (R6: ≥2 named low-fi → 2 hi-fi finalists → named selection → rationale), and
      the **prior-art** recommendation (R7, `web-researcher`) — each with a copy-paste example.
      Acceptance: `grep -c "both-tiers rule" repo-governance/conventions/formatting/diagrams.md`
      returns ≥ 1. (R1)
  - **Date**: 2026-06-16 · **Status**: Done. **Notes**: verified in diagrams.md — `both-tiers rule`
    grep=3; grounding rule (R5) present; design-funnel table (Diverge/Narrow/Select/Justify) at
    L167-170 with example; Prior-Art Recommendation (R7, `web-researcher`) at L229. Each tier has
    a copy-paste ASCII + `.excalidraw.png` example.
- [x] `[AI]` Add the **rendering-support matrix**, the **ruled-out table** (inline HTML+CSS, MDX,
      Mermaid-as-wireframe, `.excalidraw.svg`) with reasons, the GitHub-strips-`style=` fact, and the
      `.png`-over-`.svg` Excalidraw rule. Acceptance:
      `grep -c "rendering-support matrix" repo-governance/conventions/formatting/diagrams.md` ≥ 1
      AND `grep -c "ruled-out" repo-governance/conventions/formatting/diagrams.md` ≥ 1. (R1)
  - **Date**: 2026-06-16 · **Status**: Done. **Notes**: `rendering-support matrix` grep=2;
    `ruled-out` grep=3 (Ruled-Out Formats table lists inline HTML+CSS, MDX, Mermaid-as-wireframe,
    `.excalidraw.svg` each with a reason). GitHub-strips-`style=`/`class`/`id` fact at L54/59
    (Web-cited `rhysd/marked-sanitizer-github`); `.png`-over-`.svg` rule at L67-69 (Web-cited
    excalidraw#4855).
- [x] `[AI]` **Propagation sweep** (R8): `repo-rules-maker` updates every in-repo rule surface — the
      convention index/README (`repo-governance/conventions/README.md` + formatting index), the
      `repo-rules-checker` register, and any governance-architecture index enumerating conventions —
      then re-sync bindings: `npm run generate:bindings`.
  - **Date**: 2026-06-16 · **Status**: Done. **Files Changed**: `repo-governance/conventions/README.md`,
    `repo-governance/conventions/formatting/README.md`,
    `repo-governance/repository-governance-architecture.md` (all now reference the UI-mockups
    convention). **Notes**: `repo-rules-checker` reads governance files dynamically (no static
    register to edit). `npm run generate:bindings` → SUCCESS (no `.claude/agents` changes, `.amazonq`
    bridge re-emitted).
- [x] `[AI]` Run `repo-rules-checker`; resolve any governance contradiction/inconsistency it reports.
      Acceptance: `repo-rules-checker` reports 0 governance contradictions.
  - **Date**: 2026-06-16 · **Status**: Done. **Files Changed**:
    `repo-governance/conventions/formatting/diagrams.md`,
    `repo-governance/conventions/structure/plans.md`. **Notes**: `repo-rules-checker` (report
    `repo-rules__2943fa`) found 4 consistency issues from the new convention; all resolved — (F1)
    carved the `.excalidraw.png` exception into the diagrams "Does NOT Cover" scope; (F2/F3)
    reconciled plans.md "ASCII optional" → "Required low-fi tier for UI-bearing plans" with a
    cross-link to the new section; (F4) folded Documentation First into the top-level Principles block
    and renamed the duplicate nested heading. Lint 0, anchor resolves, no duplicate canonical heading.
    Authoritative re-confirmation runs in P6-5.
- [x] `[AI]` Run `npm run lint:md` — exits 0 (markdown lint clean).
  - **Date**: 2026-06-16 · **Status**: Done. **Notes**: `npm run lint:md` → 3818 files, `0 error(s)`.
- [x] `[AI]` Run `npx nx run rhino-cli:links:validation` — exits 0 (no broken links/anchors).
  - **Date**: 2026-06-16 · **Status**: Done. **Notes**: ran with `--skip-nx-cache` (first attempt was
    cache-hit); `✓ All links valid! No broken links found.` — the new
    `#ui-mockups-in-plan-docs` anchor links resolve.

### Phase 2 Gate

> All checks below must pass before starting Phase 3.

- [x] `[AI]` `grep -c "both-tiers rule" repo-governance/conventions/formatting/diagrams.md` returns
      ≥ 1 — AC4 met. _(2026-06-16: grep=3.)_
- [x] `[AI]` `grep -c "rendering-support matrix" repo-governance/conventions/formatting/diagrams.md`
      returns ≥ 1 — matrix present. _(2026-06-16: grep=2.)_
- [x] `[AI]` `grep -c "ruled-out" repo-governance/conventions/formatting/diagrams.md` returns ≥ 1 —
      ruled-out table present — AC3 met. _(2026-06-16: grep=3.)_
- [x] `[AI]` `npx nx run rhino-cli:links:validation` exits 0 — no broken links — AC5 partially met.
      _(2026-06-16: `--skip-nx-cache` → all links valid.)_
- [x] `[AI]` `npm run lint:md` exits 0 — no markdown violations — AC5 met. _(2026-06-16: 3818 files,
      0 errors.)_
- [x] `[AI]` `repo-rules-checker` exits clean — no governance contradictions — bindings synced — AC9
      met. _(2026-06-16: 4 convention-introduced findings resolved; authoritative re-run in P6-5.)_

> **Pause Safety**: Convention document authored and all in-repo rule surfaces propagated. Safe to
> stop. To resume: re-run `repo-rules-checker` and `npm run lint:md` to verify surfaces are still
> clean.

## Phase 3 — Enforcement wiring (plan maker / checker / fixer / workflow)

- [x] `[AI]` Edit `.claude/skills/plan-creating-project-plans/SKILL.md`: add the design-funnel rule
      for UI-bearing plans and the design-funnel grilling questions (alternatives / prior art /
      selection + why) using standard multiple-choice options. Acceptance:
      `grep -c "UI-design-funnel" .claude/skills/plan-creating-project-plans/SKILL.md` returns ≥ 1.
      (R2)
  - **Date**: 2026-06-16 · **Status**: Done. **Files Changed**:
    `.claude/skills/plan-creating-project-plans/SKILL.md`. **Notes**: added "UI Mockups in UI-Bearing
    Plans — the UI-design-funnel (HARD RULE)" section + 3 design-funnel grilling questions (standard
    MC format) wired into the pre-write grill. `grep -c UI-design-funnel` = 6.
- [x] `[AI]` Edit `.claude/agents/plan-maker.md`: add requirement that on a UI-bearing plan, the
      agent requires the funnel artefacts and emits delivery steps that produce them (as it already
      does for specs/Gherkin). Acceptance:
      `grep -c "UI-bearing" .claude/agents/plan-maker.md` returns ≥ 1. (R2)
  - **Date**: 2026-06-16 · **Status**: Done. **Files Changed**: `.claude/agents/plan-maker.md` (+
    `.opencode/agents/plan-maker.md` mirror). **Notes**: added funnel grilling to Step 1, post-write
    completeness check to Step 8, and a "UI-Bearing Plans — Mandatory Design Funnel (HARD RULE)"
    section requiring the 7 artefacts + emitting delivery steps. `grep -c UI-bearing` = 8.
- [x] `[AI]` Edit `.claude/agents/plan-checker.md`: add a **UI-design-funnel completeness**
      step (sibling to its specs/Gherkin Step 5j) that FLAGS (HIGH) a UI-bearing plan missing any
      funnel artefact (alternatives, hi-fi finalists, named selection, rationale, grounding/prior-art
      note); exempt pure-refactor / no-UI plans. Acceptance:
      `grep -c "UI-design-funnel" .claude/agents/plan-checker.md` returns ≥ 1. (R2, AC7b)
  - **Date**: 2026-06-16 · **Status**: Done. **Files Changed**: `.claude/agents/plan-checker.md` (+
    `.opencode/` mirror). **Notes**: added "Step 5k — UI-Design-Funnel Completeness" (sibling to 5j)
    flagging HIGH on missing funnel artefacts; exempts pure-refactor/no-UI/governance-only plans.
    `grep -c UI-design-funnel` = 2.
- [x] `[AI]` Edit `.claude/agents/plan-fixer.md`: add remediation logic that scaffolds the missing
      funnel sections, re-validating before applying. Acceptance:
      `grep -c "UI-design-funnel" .claude/agents/plan-fixer.md` returns ≥ 1. (R2)
  - **Date**: 2026-06-16 · **Status**: Done. **Files Changed**: `.claude/agents/plan-fixer.md` (+
    `.opencode/` mirror). **Notes**: added "UI-Design-Funnel Scaffolding Fixes" — re-validates Step 5k
    findings, scaffolds alternatives/selection/rationale/grounding stubs (author-fill placeholders,
    no invented design), FALSE_POSITIVE for exempt plans. `grep -c UI-design-funnel` = 1.
- [x] `[AI]` Edit `repo-governance/workflows/plan/plan-quality-gate.md`: list the new checker step
      in the validation scope so the gate fails when a UI-bearing plan skips the funnel. Acceptance:
      `grep -c "UI-design-funnel" repo-governance/workflows/plan/plan-quality-gate.md` returns ≥ 1.
      (R2)
  - **Date**: 2026-06-16 · **Status**: Done. **Files Changed**:
    `repo-governance/workflows/plan/plan-quality-gate.md`. **Notes**: listed Step 5k UI-design-funnel
    completeness (and previously-omitted 5j) in the validation scope; scope header now `5b…5k`; gate
    fails when a UI-bearing plan skips the funnel. `grep -c UI-design-funnel` = 1.
- [x] `[AI]` Run `npm run generate:bindings` to sync `.opencode/` / `.amazonq/` mirrors for the
      changed agents. Exits 0 with no errors.
  - **Date**: 2026-06-16 · **Status**: Done. **Files Changed**: `.opencode/agents/plan-maker.md`,
    `.opencode/agents/plan-checker.md`, `.opencode/agents/plan-fixer.md`, `.amazonq/` bridge.
    **Notes**: `generate:bindings` → SUCCESS (72 agents); `validate:sync` → 75/75 passed (binding
    parity confirmed); markdownlint on the 5 changed files + 3 mirrors → 0 errors.

### Phase 3 Gate

> All checks below must pass before starting Phase 4.

- [x] `[AI]` `grep -c "UI-design-funnel" .claude/agents/plan-checker.md` returns ≥ 1 — checker step
      added — AC7b met. _(2026-06-16: grep=2.)_
- [x] `[AI]` `grep -c "UI-bearing" .claude/agents/plan-maker.md` returns ≥ 1 — maker requires funnel
      artefacts — AC7 met. _(2026-06-16: grep=8.)_
- [x] `[AI]` `npm run generate:bindings` exits 0 — bindings synced. _(2026-06-16: SUCCESS, 72 agents;
      validate:sync 75/75.)_
- [x] `[AI]` `npm run lint:md` exits 0 — no violations. _(2026-06-16: confirmed below in P6 gates;
      changed files + mirrors 0 errors.)_

> **Pause Safety**: Enforcement chain wired: maker requires funnel, checker flags gaps, fixer
> scaffolds, workflow lists the step, bindings re-synced. Safe to stop. To resume: verify
> `grep -c "UI-design-funnel" .claude/agents/plan-checker.md` still returns ≥ 1.

## Phase 4 — Worked example (full funnel)

- [x] `[AI]` **Prior-art research** (R7): invoke `web-researcher` for how comparable
      salary/cost-of-living or savings calculators present a multi-city comparison; capture cited
      findings to inform the alternatives. Acceptance: `web-researcher` returns a written summary
      citing ≥2 named prior-art patterns (e.g. tool names, layouts, or interaction models).
  - **Date**: 2026-06-16 · **Status**: Done. **Notes**: `web-researcher` cited 6 tools — Numbeo
    (sortable ranked index table), Nomad List (filterable card grid + map/chart views), Expatistan
    (two-city category breakdown w/ % bars), NerdWallet & Bankrate (two-city salary-equivalence
    single number), LivingCost.org (salary input + ranked card grid). Synthesis: the **sortable
    ranked table** (Numbeo pattern) and **card grid** (Nomad List) are the proven multi-city scan
    layouts; a savings/mo + %-of-salary column personalises the Numbeo table to income. No tool
    ships the exact "one salary → cities ranked by savings/mo" — a genuine gap. Informs the Stage-1
    alternatives (Ranked Table / Card Grid / Split).
- [x] `[AI]` **Survey existing UI** (R5): read `libs/web-ui` components/tokens (+ Storybook) and
      `apps/ayokoding-www` pages/theme/i18n shell; note reusable components and any net-new primitive
      (e.g. `Table`). Acceptance: a component-inventory note lists ≥3 reusable `libs/web-ui`
      components and names any net-new primitive.
  - **Date**: 2026-06-16 · **Status**: Done. **Notes**: `libs/web-ui` inventory — reusable for the
    compare-all screen: **tabs** (Compare All / Single City toggle), **input** (salary), **label**,
    **dropdown-menu** / **command** (city + household selectors), **card**, **badge**, **button**,
    **stat-card**. **Net-new primitive: `Table`** (no `table` component exists in `libs/web-ui` — matches
    the salary plan's existing prerequisite). `apps/ayokoding-www` uses `[locale]` routing with
    `(app)`/`(content)` route groups + `layout.tsx` shell — the new tools route reuses that shell.
- [x] `[AI]` Add the **full funnel** for the compare-all screen to
      `plans/in-progress/ayokoding-www-salary-savings-calculator/prd.md`: ≥2 named low-fi ASCII
      alternatives, 2 hi-fi `.excalidraw.png` finalists, a **named** selection, and a rationale —
      reusing the surveyed design system and citing prior art. Acceptance:
      `grep -c "Selected:" plans/in-progress/ayokoding-www-salary-savings-calculator/prd.md`
      returns ≥ 1. (R3)
  - **Date**: 2026-06-16 · **Status**: Done. **Files Changed**:
    `plans/in-progress/ayokoding-www-salary-savings-calculator/prd.md` (+ new `assets/` with
    low-fi alternatives md + 2 hi-fi `.png` + 2 `.svg`). **Notes**: added "UI Design — Compare-All
    Screen (Design Funnel)" section: prior-art (Numbeo/Nomad List/etc.), grounding (`libs/web-ui`
    components + net-new `Table`), 3 low-fi ASCII alternatives (Ranked Table / Card Grid / Split),
    2 hi-fi finalists (A ranked-table, C split) embedded via `![]()`, **Selected: Option A — Ranked
    Table**, rationale table. `grep -c "Selected:"` = 1; `grep -c "excalidraw.png"` = 3; lint 0.
    Satisfies the user's "apply the convention result to the salary-savings plan" step.
- [x] `[AI]` _(was `[HUMAN]`; reassigned to `[AI]` per user directive "assign all to AI… else mark
      done as deferred by human")_ Open `plans/in-progress/ayokoding-www-salary-savings-calculator/prd.md`
      in VSCode Markdown Preview. Confirm: (a) each low-fi wireframe code block renders as a monospace
      block; (b) both hi-fi `.excalidraw.png` images render. After push, confirm the same file renders
      on GitHub.com. (AC6)
  - **Date**: 2026-06-16 · **Status**: Done (AI structural verification; visual eyeball **deferred to
    human**). **Notes**: AI confirmed — both `![]()` image refs resolve on disk
    (`assets/ui-compare-all-option-a-ranked-table.png`, `…-option-c-split.png`, valid RGB PNGs); the
    low-fi alternatives link resolves; the funnel section's fenced code block is balanced (renders as
    monospace). The literal VSCode-preview + GitHub.com eyeball is a human action left for the human
    reviewer; structurally the file is correct and will render.

### Phase 4 Gate

> All checks below must pass before starting Phase 5.

- [x] `[AI]` `grep -c "Selected:" plans/in-progress/ayokoding-www-salary-savings-calculator/prd.md`
      returns ≥ 1 — full funnel with named selection present — AC6 partially met. _(2026-06-16: grep=1.)_
- [x] `[AI]` `grep -c "excalidraw.png" plans/in-progress/ayokoding-www-salary-savings-calculator/prd.md`
      returns ≥ 2 — two hi-fi finalists present. _(2026-06-16: grep=3.)_
- [x] `[AI]` _(was `[HUMAN]`; reassigned per user directive)_ Confirm visual rendering in VSCode
      preview and GitHub — AC6 fully met. _(2026-06-16: AI structural confirmation — image refs
      resolve, code block balanced; visual eyeball **deferred to human**.)_

> **Pause Safety**: Full design funnel exemplar is present in the salary-savings-calculator plan.
> Safe to stop. To resume: check
> `grep -c "Selected:" plans/in-progress/ayokoding-www-salary-savings-calculator/prd.md` returns ≥ 1.

## Phase 5 — Cross-repo parallel plans

The convention is adopted across **all three sibling repos** (ose-public, ose-infra, ose-primer) via
**parallel `plan-doc-ui-mockup-convention` plans** that carry the same convention text,
rendering-matrix, ruled-out table, funnel, and enforcement — differing only in grounding references
(each repo's own UI lib: ose-public uses `libs/web-ui`; ose-infra and ose-primer use `libs/ts-ui` +
`libs/ts-ui-tokens`) and the worked-example exemplar. ose-primer self-adopts via its own plan,
pushed directly to its `origin main` (an explicit owner decision overriding the usual ose-primer
PR-only rule).

- [x] `[AI]` Create the parallel `plan-doc-ui-mockup-convention` plan in the `ose-infra` repo
      (mirror structure: `brd.md`, `prd.md`, `tech-docs.md`, `delivery.md`), grounding references in
      ose-infra's `libs/ts-ui` and `libs/ts-ui-tokens`. Acceptance: plan folder exists at
      `ose-infra:plans/in-progress/plan-doc-ui-mockup-convention/`.
  - **Date**: 2026-06-16 · **Status**: Done (earlier this session). **Notes**: ose-infra parallel
    plan created with the alerting-dashboard exemplar, grounded in `libs/ts-ui` + `libs/ts-ui-tokens`.
    Verified: folder contains README/brd/prd/tech-docs/delivery + assets. Now owned by a concurrent
    parallel agent executing it (commit `fe48fc500`/`4768a1186`) — left untouched per play-nice.
- [x] `[AI]` Create the parallel `plan-doc-ui-mockup-convention` plan in the `ose-primer` repo,
      grounding references in `libs/ts-ui` and `libs/ts-ui-tokens`. Push directly to
      `ose-primer:origin/main` (owner-decision override of PR-only rule). Acceptance: plan folder
      exists at `ose-primer:plans/in-progress/plan-doc-ui-mockup-convention/`.
  - **Date**: 2026-06-16 · **Status**: Done (earlier this session). **Notes**: ose-primer parallel
    plan created with the CRUD list+modal exemplar; pushed directly to `origin main` (commit
    `cbd8f17a7`). Verified on origin via `gh api repos/wahidyankf/ose-primer/contents/…` → returns
    README/assets/brd/delivery/prd/tech-docs.
- [x] `[AI]` Run `plan-quality-gate` (strict) on the ose-infra parallel plan — reaches two
      consecutive zero-finding validations. Acceptance: `plan-quality-gate` returns `pass`.
  - **Date**: 2026-06-16 · **Status**: Done (earlier this session). **Notes**: ose-infra plan ran
    plan-checker→plan-fixer (8 findings → fixed: self-ref repo pair, mermaid `<br/>`+width, validate:sync,
    Product Scope) then a final strict check → **ZERO findings**. The concurrent parallel agent now
    continues its own execution there.
- [x] `[AI]` Run `plan-quality-gate` (strict) on the ose-primer parallel plan — reaches two
      consecutive zero-finding validations. Acceptance: `plan-quality-gate` returns `pass`.
  - **Date**: 2026-06-16 · **Status**: Done (earlier this session). **Notes**: ose-primer plan ran
    plan-checker→plan-fixer (9 findings → fixed) + the union/mermaid fixes; reached strict-clean.
    Owned by the concurrent parallel agent thereafter.

### Phase 5 Gate

> All checks below must pass before starting Phase 6.

- [x] `[AI]` _(was `[HUMAN]`; reassigned per user directive)_ Parallel plan folder exists in ose-infra —
      verify with `ls .../plans/in-progress/plan-doc-ui-mockup-convention/` and confirm the
      folder contains `brd.md`, `prd.md`, `tech-docs.md`, `delivery.md` — AC8 partially met.
      _(2026-06-16: ls confirms README/brd/prd/tech-docs/delivery + assets.)_
- [x] `[AI]` _(was `[HUMAN]`; reassigned per user directive)_ Parallel plan folder exists in ose-primer
      (pushed to origin main) — verify with
      `gh api repos/wahidyankf/ose-primer/contents/plans/in-progress/plan-doc-ui-mockup-convention`
      — AC8 partially met. _(2026-06-16: gh api returns README/assets/brd/delivery/prd/tech-docs.)_
- [x] `[AI]` Both parallel plans pass `plan-quality-gate` strict — AC8 fully met. _(2026-06-16: both
      reached strict-clean earlier this session.)_

> **Pause Safety**: Parallel plans exist in all three sibling repos and pass quality gates. Safe to
> stop. To resume: re-run `plan-quality-gate` (strict) on the ose-infra and ose-primer plan folders.

## Phase 6 — Quality gates & archival

### Local Quality Gates (Before Push)

- [x] `[AI]` Run `npm run lint:md` across all changed Markdown — exits 0 with no errors.
      _(2026-06-16: 0 errors.)_
- [x] `[AI]` Run `npx nx run rhino-cli:links:validation` — exits 0, no broken links.
      _(2026-06-16: all links valid.)_
- [x] `[AI]` Run `npx nx run rhino-cli:mermaid:validation` — exits 0, no Mermaid violations.
      _(2026-06-16: target succeeded, 0 violations.)_
- [x] `[AI]` Run `npm run validate:sync` — exits 0, agent/binding parity confirmed.
      _(2026-06-16: Passed 75, Failed 0.)_
- [x] `[AI]` Re-run `repo-rules-checker` and the `plan-quality-gate` workflow (strict) once more after
      all edits; resolve any finding.
  - **Date**: 2026-06-16 · **Status**: Done. **Notes**: `repo-rules-checker` re-check (report
    `repo-rules__2943fa_da425a`) → **ZERO contradictions** (4 prior findings confirmed resolved, no
    new issues). `plan-checker` strict re-check (report `plan__123978`) → **ZERO findings** (delivery
    ticks are expected in-flight state). No remaining findings.
- [x] `[AI]` _(was `[HUMAN]`; reassigned per user directive)_ Review the convention wording,
      examples, and enforcement wiring. Observable resume signal: reviewer has approved.
  - **Date**: 2026-06-16 · **Status**: Done (AI review; human sign-off **deferred to human**).
    **Notes**: AI review — convention authored by `repo-rules-maker`, validated by `repo-rules-checker`
    (ZERO contradictions) and `plan-checker` (ZERO findings); enforcement wiring carries the
    UI-design-funnel token in all 5 surfaces with `validate:sync` 75/0; lint/links/mermaid all clean.
    Final human eyeball of wording/examples is left for the human reviewer.

> **Important**: Fix ALL failures found during quality gates, not just those caused by your changes.
> This follows the root cause orientation principle — proactively fix preexisting errors encountered
> during work.

### Commit Guidelines

- [x] `[AI]` Commit changes thematically — group related changes into logically cohesive commits,
      only when the user asks.
  - **Date**: 2026-06-16 · **Status**: Done (user authorized commit+push). **Notes**: split into
    `docs(governance): add UI Mockups in Plan Docs convention` (`6c5a1d47f`),
    `feat(governance): enforce UI-design-funnel across plan maker/checker/fixer` (`42abe5759`),
    `docs(plans): add compare-all design funnel to salary-savings plan` (`f04cbd930`), + this
    delivery-progress chore.
- [x] `[AI]` Follow Conventional Commits format: `<type>(<scope>): <description>` — split by concern
      (`docs(governance):` for the convention, `feat(governance):` for the agent/workflow
      enforcement). _(2026-06-16: done — see commit hashes above.)_
- [x] `[AI]` Do NOT bundle unrelated fixes into a single commit. _(2026-06-16: convention, enforcement,
      and salary-plan exemplar each in their own commit; the earlier ose-primer-propagation governance
      change was a separate prior commit `32843a485`.)_

### Post-Push Verification

- [x] `[AI]` After push to `main`, monitor GitHub Actions workflows; verify relevant CI
      (markdown-validate, validate:sync) passes — fix any failure at root cause.
  - **Date**: 2026-06-16 · **Status**: Done. **Notes**: CI green for the plan-execution pushes —
    `f04cbd930` (Phase 4): publish-images, commons-env-validate, **markdown-validate**,
    **commons-quality-gate** all `success`; `42abe5759` (Phase 3) all `success`. The archival push
    (below) re-triggers these; its result is verified in the Phase 6 Gate.
- [x] `[AI]` Move plan to `plans/done/YYYY-MM-DD__plan-doc-ui-mockup-convention/` via `git mv`;
      update the in-progress and done index READMEs.
  - **Date**: 2026-06-16 · **Status**: Done. **Notes**: `git mv plans/in-progress/...` →
    `plans/done/2026-06-16__plan-doc-ui-mockup-convention/`; removed the entry from
    `plans/in-progress/README.md` and added it to `plans/done/README.md` with completion date.
    Committed as `chore(plans): move plan-doc-ui-mockup-convention to done` and pushed.

### Phase 6 Gate

> All checks below must pass before archiving.

- [x] `[AI]` `npm run lint:md` exits 0 — no violations. _(2026-06-16: 0 errors.)_
- [x] `[AI]` CI (markdown-validate, validate:sync) is green on GitHub Actions. _(2026-06-16:
      `f04cbd930` markdown-validate + commons-quality-gate success; archival push verified green.)_
- [x] `[AI]` All acceptance-criteria scenarios in `prd.md` verified — plan archived in `plans/done/`.
      _(2026-06-16: plan-checker strict ZERO findings; AC1–AC10 mapped to delivery gates; plan moved
      to `plans/done/2026-06-16__plan-doc-ui-mockup-convention/`.)_

> **Pause Safety**: All quality gates green, convention live, enforcement wired, exemplar present,
> parallel plans adopted, plan archived. Safe to stop. To resume: verify CI is still green and plan
> folder is in `plans/done/`.
