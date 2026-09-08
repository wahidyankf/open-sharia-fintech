---
description: "Forcing-functions 5-6: usability probes, recurrence/diff/completeness critic."
when_to_use: "Use when applying the usability-probe or recurrence-critic forcing-function."
---

# The Six Forcing-Functions (5-6)

## 5. Usability Probes

Apply all five probes on every run. A probe that applies to only some surfaces must still be
applied on all surfaces where it could apply.

**5a. Conditional / Hidden-Control Discoverability**: Identify every control that is hidden,
collapsed, or conditionally rendered. For each, verify that a first-time user can discover its
existence and purpose without prior knowledge. A control whose existence is not surfaced through
any visible affordance is a discoverability defect (Nielsen Heuristic 6: Recognition rather than
recall; NN/g Progressive Disclosure).

**5b. Per-Label Jargon Scan**: Read every visible label, heading, tooltip, placeholder, and
button text. Flag any term that a first-time user -- unfamiliar with the domain -- could not
interpret from context alone (Nielsen Heuristic 2: Match between system and real world).

**5c. Cross-View Redundancy**: Identify any element that appears on multiple views and conveys
identical information. Flag it as a redundancy defect (Nielsen Heuristic 8: Aesthetic and
minimalist design; Hick's Law: excess choices increase decision time).

**5d. Input Unit and Currency Consistency**: For every input that accepts a numeric value with
a unit (currency, percentage, distance, weight), verify that:

- The unit is stated adjacent to the input or its label (not hidden or absent).
- If a currency symbol is shown, it reflects the user's selected currency, not a hardcoded
  default (Nielsen Heuristic 5: Error prevention; WCAG 2.2 SC 3.3.2 Labels or Instructions;
  Nielsen Heuristic 4 cross-surface consistency).

**Ground**: Nielsen Heuristics 2, 4, 5, 6, 8; NN/g Progressive Disclosure; Hick's Law;
WCAG 2.2 SC 3.3.2 Labels or Instructions.

## 6. Recurrence + Diff Memory + Completeness Critic

**Obligation**: Every test run must carry forward knowledge from prior runs and challenge itself
to achieve completeness.

**6a. Recurrence check**: At the start of each run, list the defect _classes_ found in prior
runs (not just individual findings). For each class, re-verify the same class of element
on every surface. A defect class that was fixed in one location but not in analogous locations
is a partial fix.

**6b. Diff memory**: Note what changed since the last test run (from the plan's delivery
checklist or git log). Re-verify all surfaces adjacent to or dependent on the changed
components -- not only the changed components themselves.

**6c. Completeness critic**: End every run with an explicit self-audit: "What did we NOT
enumerate?" List the surface categories (tabs, breakpoints, locales, control types) and
verify each was covered. A category not enumerated is an open gap, not an implicit pass.

**Ground**: Regression-test mandate (prior defect classes must be rechecked); differential
testing principle (changes create adjacency risk); Deliberate Problem-Solving principle.
