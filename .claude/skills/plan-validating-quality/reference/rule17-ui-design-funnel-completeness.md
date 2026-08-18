# Rule 17: UI-Design-Funnel Completeness (Step 5k — MANDATORY)

Enforces the
[UI Mockups in Plan Docs convention](../../../../repo-governance/conventions/formatting/diagrams/ui-mockups-principles-and-scope.md#ui-mockups-in-plan-docs-principles-in-practice-and-scope)
— the sibling of the specs/Gherkin Step 5j: a UI-bearing plan (adds/changes/replaces user-facing
screens or components under `apps/**`/`libs/**`) must carry the design funnel.

**What to validate**:

1. **Scope detection** — determine UI-bearing status from Scope, file-impact, and delivery steps; if
   not UI-bearing, skip (no findings).
2. **Funnel placement in `prd.md` (HARD RULE)** — all funnel artefacts (low-fi wireframes, hi-fi
   `![]()` embeds, named selection, rationale table) live in `prd.md`; binary mockup assets under the
   plan's `assets/` folder. `prd.md` missing the funnel, or funnel present only elsewhere: **HIGH**.
   See
   [UI Mockups in Plan Docs — Placement](../../../../repo-governance/conventions/formatting/diagrams/ui-mockups-placement-hard-rule-requirements.md#placement--the-ui-lives-in-prdmd-hard-rule-requirements-and-enforcement).
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
