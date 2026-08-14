# Rules 16-18: Specs/Gherkin Coverage, Regression Tests, UI Funnel, Knowledge Capture

## 16. Specs and Gherkin Delivery Coverage (Step 5j — MANDATORY)

Enforces the
[Feature Change Completeness Convention §Two Paths](../../../../repo-governance/development/quality/feature-change-completeness.md)
for the plan path: a plan creating, modifying, or deleting observable behavior in `apps/`, `libs/`,
or `specs/` MUST carry explicit steps adding/updating companion `specs/` `.feature` files and running
`specs:coverage`.

**What to validate**:

1. **Scope detection** — from Scope (`README.md`/`prd.md`), file-impact (`tech-docs.md`), and delivery
   steps, determine whether observable behavior under `apps/**`, `libs/**`, or `specs/**` is created,
   modified, or deleted.
2. **Specs/Gherkin authoring step present** — if yes, the checklist includes at least one step
   creating/updating the relevant `specs/apps/**` or `specs/libs/**` feature file(s). Missing:
   **HIGH**.
3. **`specs:coverage` gate present** — the checklist or a phase gate runs the project's
   `specs:coverage` target. Missing: **HIGH**.
4. **Behavior-change exemption** — behavior-preserving refactors, no-behavior-change dependency bumps,
   docs/governance-only plans are exempt (mirrors Feature Change Completeness applicability). Verify
   the exemption is legitimate and stated; an illegitimate exemption is **HIGH**.

**Finding severity**: behavior-affecting plan with no specs/Gherkin step: **HIGH**. Specs step present
but no `specs:coverage` gate: **HIGH**. Step present but vague (no specific feature path/domain):
**MEDIUM**. Illegitimate "no behavior change" exemption: **HIGH**.

## 16b. Regression Test Mandate (bug-fix plans — MANDATORY)

Enforces the
[Regression Test Mandate](../../../../repo-governance/development/quality/regression-test-mandate.md):
a plan fixing discovered bugs/regressions (e.g. built from EWT/UWT/DWT findings) MUST carry an
explicit delivery step per finding adding a **reproducing test** (failing-first, pins the bug) —
Gherkin in `specs/**` plus the consuming test for behavioural defects, or a DOM/computed-style/content
test for visual/copy defects.

**What to validate**: (1) bug-fix detection — does the plan exist to fix defects? (2) per-finding
reproducing-test step — each finding's delivery steps include a failing-first test before its fix
step (RED→GREEN); missing for any finding: **HIGH**. (3) no exemption — applies to cosmetic/visual
findings too (the test form adapts, a test is still required); an untested cosmetic fix is **HIGH**.

## 17. UI-Design-Funnel Completeness (Step 5k — MANDATORY)

Enforces the
[UI Mockups in Plan Docs convention](../../../../repo-governance/conventions/formatting/diagrams/42-ui-mockups-principles-and-scope.md#ui-mockups-in-plan-docs-principles-in-practice-and-scope)
— the sibling of the specs/Gherkin Step 5j: a UI-bearing plan (adds/changes/replaces user-facing
screens or components under `apps/**`/`libs/**`) must carry the design funnel.

**What to validate**:

1. **Scope detection** — determine UI-bearing status from Scope, file-impact, and delivery steps; if
   not UI-bearing, skip (no findings).
2. **Funnel placement in `prd.md` (HARD RULE)** — all funnel artefacts (low-fi wireframes, hi-fi
   `![]()` embeds, named selection, rationale table) live in `prd.md`; binary mockup assets under the
   plan's `assets/` folder. `prd.md` missing the funnel, or funnel present only elsewhere: **HIGH**.
   See
   [UI Mockups in Plan Docs — Placement](../../../../repo-governance/conventions/formatting/diagrams/47-ui-mockups-placement-hard-rule-requirements.md#placement--the-ui-lives-in-prdmd-hard-rule-requirements-and-enforcement).
3. **Both tiers per screen** — each screen has a low-fidelity ASCII/Unicode wireframe in a fenced code
   block AND a high-fidelity `.excalidraw.png` (or approved plain `.png`) referenced via `![](./…)`,
   in separate labelled subsections. Missing a tier, or a ruled-out format (inline HTML+CSS, MDX,
   Mermaid-as-wireframe, `.excalidraw.svg`): **HIGH**.
4. **≥2 named low-fi alternatives** — the diverge stage presents at least two genuinely different named
   options (at least mobile plus desktop where they differ). None or one: **HIGH**.
5. **2 hi-fi finalists** — the narrow stage carries the strongest alternatives as hi-fi finalists.
   Missing: **HIGH**.
6. **Named selection** — the select stage names the chosen design explicitly. Unnamed/implicit:
   **HIGH**.
7. **Rationale/decision record** — the justify stage includes a short rationale (a table suffices):
   why the winner won, why each runner-up lost. Missing: **HIGH**.
8. **Grounding/prior-art note** — the R5 grounding note (surveyed `libs/web-ui`/target app/sibling
   screens, net-new components named) and the R7 prior-art citation (`web-researcher` survey). Missing
   either: **HIGH**.
9. **Responsive strategy** — mobile-first across mobile (`< sm`), tablet (`md` ≥ 768px), desktop (`lg`
   ≥ 1024px); the decision record states which components stack/collapse/hide/change per breakpoint;
   low-fi tier shows the mobile↔desktop reflow where it differs. No stated strategy, or desktop-only
   evaluated finalists: **HIGH**.
10. **Exemption** — pure-refactor/no-UI/governance-only plans EXEMPT (mirrors specs/Gherkin
    exemption). Verify legitimacy; illegitimate exemption on a genuinely UI-bearing plan: **HIGH**.

**Finding severity**: `prd.md` missing the funnel entirely, or funnel misplaced: **HIGH**. Missing any
funnel artefact: **HIGH**. No responsive strategy, or desktop-only finalists: **HIGH**. Artefact
present but vague (alternatives not genuinely different, no drop reasons): **MEDIUM**. Illegitimate
"no UI" exemption: **HIGH**. Non-UI/pure-refactor/governance-only plan: not flagged.

## 18. Knowledge Capture Phase Presence (Step 5l — MANDATORY)

Enforces the
[Knowledge Capture Convention](../../../../repo-governance/development/quality/knowledge-capture.md):
every substantive plan's `delivery.md` carries a final Knowledge Capture phase triaging the transient
`learnings.md` log — through the open-ended principle-based triage rubric, the code-routing rule, and
both safety gates — before archival.

**What to validate**:

1. **Phase presence** — a phase referencing triaging `learnings.md` against the routing matrix and
   both safety gates, positioned as the FINAL substantive phase, immediately before Plan Archival.
2. **Explicit "none" record PASSES** — a `No generalizable learnings — <reason>` escape is a PASS, not
   a finding; only silence is penalized.
3. **Silent absence is the only violation** — no phase AND no explicit "none" record anywhere:
   **MEDIUM**, per
   [Criticality Levels Convention](../../../../repo-governance/development/quality/criticality-levels.md).
4. **Code-routing rule stated** — the phase states a learning routed to `apps/`/`libs/`/tests is
   ALWAYS filed as a separate `plans/backlog/` plan, never landed inline (current-plan-blocker
   carve-out aside). Missing: **MEDIUM**.
5. **Both safety gates present** — references applying the secret/sensitivity gate and the
   repo-relevance gate to every surviving entry. Missing either: **MEDIUM**.
6. **`plans/ideas/` overlap-scan rule stated** — if the routing matrix names `plans/ideas/` (default),
   the phase states any entry routed there is checked against `plans/ideas/README.md` and existing
   two-pagers first, folding in rather than duplicating, per
   [Integrate Before You Add](../../../../repo-governance/conventions/structure/plans/03-ideas-folder-overview-rationale-and-file-layout.md#integrate-before-you-add-no-duplicate-two-pagers).
   Silent: **MEDIUM**.
7. **Exemption** — pure-docs/trivial plans may skip an elaborate phase; the explicit "none" escape
   satisfies it. Illegitimate exemption on a substantive plan: **MEDIUM**.

**Finding severity**: no phase and no "none" record: **MEDIUM**. Explicit "none" record present: PASS
(not a finding). Phase present but missing the code-routing rule, either safety-gate reference, or
the `plans/ideas/` overlap-scan rule: **MEDIUM**. Illegitimate trivial-plan exemption: **MEDIUM**.
