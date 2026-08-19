# Design Dimensions Checklist

Apply the dimensions relevant to the goal; record which were covered and which were not.

- **Mockup fidelity** — the rendered layout, sizing, and element placement match the committed mockups
  at each breakpoint; nothing is missing, displaced, or restyled away from the design.
- **Runtime token fidelity** — computed colours, spacing, radii, shadows, and type read from the theme
  tokens; no raw/off-scale/inline-overridden values reach the rendered page.
- **Design-system-primitive reuse** — components that the shared library provides are actually used;
  no reinvented bespoke equivalent of a `libs/web-ui` primitive.
- **Visual hierarchy & emphasis** — the intended primary element is visually dominant; secondary/
  tertiary elements recede as designed.
- **Alignment & grid** — elements align to the intended grid/baseline; no accidental off-grid drift.
- **Spacing & density (not cramped)** — whitespace follows the spacing scale; the layout is not
  cramped; groupings reflect relatedness (Gestalt proximity).
- **Typography** — type scale, weight, line-height, and measure match the system; no overflow/
  truncation; per-locale text length handled gracefully.
- **Colour & state styling** — palette fidelity; correct hover/active/focus/disabled token usage;
  intended contrast preserved.
- **Cross-surface visual consistency** — the same component/datum looks consistent across sibling
  pages, locales, breakpoints, and repeat visits; shared chrome agrees.
- **Responsive design fidelity** — at each breakpoint the design adapts as the mockups intend (not
  merely "does not break"); intended responsive transformations match the design.
- **External-source parity** — when an external design source was provided, the live page matches it.
