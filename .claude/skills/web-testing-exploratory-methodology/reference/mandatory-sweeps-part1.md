# Mandatory Systematic Sweeps (Forcing Functions), Part 1: Sweeps A and B

The dimension checklist gives **breadth**; these three sweeps give **exhaustiveness**. They are not
optional charters — every `standard` and `thorough` run MUST execute all three and record their
matrices in the `README.md` coverage map. They exist because dimension-and-tour testing reliably
finds _representative_ defects yet repeatedly misses the "enumerate every element and assert one
property" class: a shared control that no-ops on one surface, an input whose state never reaches the
URL, an invariant the app declares but only half-implements. **Enumerate; do not sample.** A sampled
or empty matrix is not coverage.

**Grounding**: sweep A cites Nielsen **Heuristic 4 (Consistency & Standards)** and **WCAG 2.2 SC
3.2.4 (Consistent Identification)** — same-function components must be identified/behave consistently
across pages (technique G197). Sweep B cites the **MDN History API** state contract — every
`pushState` URL must, loaded cold, reproduce the same view state — plus Heuristics 1 (Visibility of
system status) and 3 (User control & freedom: back/forward must work).

## A. Shared-control × surface matrix (consistency by enumeration)

1. Enumerate EVERY shared / global control — filters, scope selectors, segmented toggles, search,
   sort, household/quantity inputs, currency and locale switchers — i.e. any control that appears on,
   or is meant to affect, more than one tab / view / surface.
2. Enumerate every surface that control is meant to affect (each tab, each list/table, the mobile vs
   desktop rendering, each locale).
3. For each (control × surface) cell, exercise the control and **assert its effect is present and
   matches its effect on the sibling surfaces**. A control that works on tab A but silently no-ops on
   tab B is a Major+ behavioural-consistency defect — cite the surface where it DOES work as the
   "expected".
4. Record the matrix (control rows × surface columns, ✓ / ✗ / n-a per cell) in the coverage map.

> Class this catches: _"the geographic filter scoped the Cost tab but the Savings tab ignored it."_

## B. Per-control URL / state round-trip sweep

For EVERY interactive control whose state a user could reasonably want to keep, share, or restore:

1. Change the control to a non-default value.
2. Assert the address bar updates to encode that value.
3. Reload the page — and, separately, open the resulting URL in a fresh context / new tab — and
   assert the control **and its downstream view** are restored to the changed state.
4. Exercise back / forward across a few changes and assert state tracks history.
5. Flag any control whose state is **not** reflected in the URL — **Major** when the app declares
   URL/state-restoration as an invariant (see C), otherwise a UX finding. Record a control ×
   {in-URL? / restores-on-reload? / survives-new-tab?} table in the coverage map.

> Class this catches: _"the min-role baseline inputs and the Savings gross were not in the URL even
> though sibling controls were, and a stated 'URL is the single source of truth' invariant existed."_
