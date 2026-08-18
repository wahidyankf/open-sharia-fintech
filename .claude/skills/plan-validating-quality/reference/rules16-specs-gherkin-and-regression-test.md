# Rules 16 and 16b: Specs/Gherkin Coverage and Regression Test Mandate

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
