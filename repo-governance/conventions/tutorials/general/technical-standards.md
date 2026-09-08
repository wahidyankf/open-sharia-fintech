---
description: "Defines mathematical-notation (LaTeX), code-example, file-organization, and accessibility technical standards for tutorials."
when_to_use: "Read when checking a tutorial's LaTeX formulas, code examples, file naming, or accessibility against technical standards."
---

# Technical Standards

Technical quality ensures tutorials are accurate, accessible, and maintainable.

## Mathematical Notation

**Requirements**: - Follow [Mathematical Notation Convention](../../formatting/mathematical-notation.md) — Use LaTeX for all formulas - **CRITICAL**: Display-level equations MUST use `$$` delimiters - **CRITICAL**: Single `$` ONLY for inline math (on same line as text) - **CRITICAL**: All `\begin{align}` blocks MUST use `$$` delimiters - Define all variables after formulas - Use proper mathematical typography

**Correct Display Math**:

```markdown
PASS: Correct:

$$
r_e = r_f + \beta \times (r_m - r_f)
$$

PASS: Correct (multi-line):

$$
\begin{align}
WACC &= \frac{E}{V} \times r_e + \frac{D}{V} \times r_d \times (1 - T_c) \\
     &= 0.645 \times 11.4\% + 0.355 \times 3.41\% \\
     &= 8.56\%
\end{align}
$$
```

**Incorrect Display Math**:

```markdown
FAIL: Incorrect (single $ for display):
$
r_e = r_f + \beta \times (r_m - r_f)
$

FAIL: Incorrect (single $ with align):
$
\begin{align}
WACC &= \frac{E}{V} \times r_e
\end{align}
$
```

**Why This Matters**: Single `$` on its own line causes LaTeX to display as raw text instead of rendering properly on GitHub.

## Code Examples

**Requirements**: - Complete, runnable code (not fragments) - Follow language-specific conventions - Include comments explaining logic - Show expected output - Type hints when applicable (Python, TypeScript) - Error handling for production examples

**Quality Checklist**: - [ ] Code runs without errors - [ ] Output is shown and correct - [ ] Comments explain "why" not just "what" - [ ] Variable names are clear and descriptive - [ ] Follows project style guide - [ ] No security vulnerabilities (hardcoded secrets, etc.)

## File Organization

**Naming**: - Follow [File Naming Convention](../../formatting/linking.md) — Use relative paths with `.md` extension - Link to related tutorials, how-to guides, references - Link to prerequisite material - Link to next steps

**Format**:

```markdown
For more details on the Diátaxis framework, see [Diátaxis Framework Convention](../../structure/diataxis-framework.md).

If you're new to finance, start with [Accounting](../../business-and-finance/accounting.md).
```

**Internal Links**: - Link to glossary for terms - Link to conventions for standards - Link to references for formulas - Link to how-to guides for tasks

## Accessibility

**Requirements**: - Clear headings hierarchy (H1 → H2 → H3, no skipping) - Alt text for images (if using images) - Descriptive link text (not "click here") - Sufficient color contrast (Mermaid diagrams) - Screen reader friendly LaTeX (MathJax support)

**Examples**:

```markdown
PASS: Good: See [Capital Budgeting Process](../capital-budgeting.md)
FAIL: Bad: See capital budgeting process [here](../capital-budgeting.md)

PASS: Good: ![NPV calculation flowchart showing decision logic](../images/npv-flowchart.png)
FAIL: Bad: ![](../images/npv-flowchart.png)
```
