---
description: "Forcing-functions 3-4: declared-invariant conformance, styling consistency."
when_to_use: "Use when applying the invariant-conformance or styling-consistency forcing-function."
---

# The Six Forcing-Functions (3-4)

## 3. Declared-Invariant Conformance

**Obligation**: Before testing, extract all declared invariants from the available sources:
Gherkin scenarios in `specs/**`, source-code comments (e.g., "URL is the single source of
truth"), `AGENTS.md`/`CLAUDE.md` product-requirement statements, and `prd.md` acceptance
criteria in the plan. For each invariant, verify that it holds for EVERY applicable element,
not just a sample. An invariant that holds for three of four inputs is a violated invariant.

**How to apply**:

1. List every declared invariant before testing.
2. For each invariant, enumerate every element it applies to.
3. Check each element against the invariant.
4. A single failure is a HIGH-severity finding; the invariant is violated even if all other
   instances pass.

**Ground**: Derived from the feature's own specification -- a violation is a spec-conformance
defect by definition.

## 4. Raw / Unstyled Native-Element Audit and Cross-Surface Styling Consistency Matrix

**Obligation**: Enumerate every interactive element (buttons, inputs, selects, checkboxes,
toggles, links) on every surface. For each element, record the tuple:
`(computed background-color, computed color, computed border, computed border-radius, computed
font-size)`. Assert two properties:

1. No element is rendered as a raw, unstyled native browser control while its sibling on another
   surface receives full design-system styling (raw native elements fail visual regression
   baselining and signal incomplete component migration).
2. Elements of the same semantic type (e.g., all primary action buttons) share the same computed-
   style tuple across surfaces (Nielsen Heuristic 4 internal consistency; visual-regression
   baselining).

**Ground**: Nielsen Heuristic 4 internal consistency; visual-regression baselining (Chromatic) /
computed-style tuples.
