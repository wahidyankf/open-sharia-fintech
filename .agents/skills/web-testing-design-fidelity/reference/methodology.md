# Evaluation Methodology — Design-Fidelity + Design-Practice Review

Combine two disciplines: **design-fidelity comparison** (does the rendered page match the design
ground truth?) and **design-practice review** (does it follow sound visual-design principles even
where no single mockup is violated?). Each finding cites the specific ground truth or principle it
breaks — a design finding is never a vibe.

## 1. Design-fidelity comparison

For each route × breakpoint × locale, render the live page and compare it, element by element, against
each available design ground truth (the five sources below). A divergence — wrong colour, off-scale
spacing, mismatched type, displaced element, reinvented component — is a finding whose **expected**
cites the specific source (the mockup file, the token name, the primitive).

## 2. Design-practice review (the visual-design principles)

Sweep the rendered page against the durable principles of visual design, recording every violation
with the principle it breaks:

- **Visual hierarchy** — the most important element is the most prominent; size, weight, colour, and
  position guide the eye in priority order.
- **Alignment** — elements share consistent edges/baselines; nothing is off-grid without intent.
- **Spacing & density (not cramped)** — whitespace is deliberate and consistent with the spacing scale;
  related items are grouped and unrelated items separated (Gestalt proximity); the layout breathes and
  is **not cramped** — controls, text, and touch targets are not crowded past comfortable density.
- **Typography** — the type scale, weights, line-height, and measure match the system; no orphaned
  one-off font sizes; text is not truncated or overflowing.
- **Colour & contrast** — colours come from the theme palette (not raw/off-brand values); foreground/
  background pairings read as designed; states (hover/active/disabled) use the intended tokens.
- **Consistency & repetition** — repeated components look and behave identically across the page and
  across sibling surfaces; shared chrome (nav, footer, cards) is uniform.
- **Balance & composition** — visual weight is distributed as the design intends; no accidental
  lopsidedness introduced at a breakpoint.

Where a principle's exact, current statement is in doubt, delegate to `web-researcher` rather than
guessing, and cite the principle in the finding.
