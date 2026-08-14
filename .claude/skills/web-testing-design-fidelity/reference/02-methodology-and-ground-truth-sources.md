# Evaluation Methodology and the Five Ground-Truth Sources

## Evaluation Methodology — Design-Fidelity + Design-Practice Review

Combine two disciplines: **design-fidelity comparison** (does the rendered page match the design
ground truth?) and **design-practice review** (does it follow sound visual-design principles even
where no single mockup is violated?). Each finding cites the specific ground truth or principle it
breaks — a design finding is never a vibe.

### 1. Design-fidelity comparison

For each route × breakpoint × locale, render the live page and compare it, element by element, against
each available design ground truth (the five sources below). A divergence — wrong colour, off-scale
spacing, mismatched type, displaced element, reinvented component — is a finding whose **expected**
cites the specific source (the mockup file, the token name, the primitive).

### 2. Design-practice review (the visual-design principles)

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

## The Five Ground-Truth Sources (judged on the LIVE rendered page)

Document and apply all five, each judged against the **running** page:

1. **Committed plan-folder mockup assets** — the both-tier mockups the plan-doc UI-mockup convention
   requires (`./assets/ui-<screen>-…`), per
   [UI Mockups in Plan Docs](../../../../repo-governance/conventions/formatting/diagrams/42-ui-mockups-principles-and-scope.md#ui-mockups-in-plan-docs-principles-in-practice-and-scope).
   Compare the rendered page to these and report divergence as a `DWT-###` finding citing the mockup
   file.
2. **Design tokens / theme (colours, spacing, typography) at RUNTIME** — the **runtime counterpart** to
   `swe-ui-checker`'s static source check. Read computed styles on the live page and compare them to
   the theme tokens; an inline-overridden colour or off-scale spacing that the source check cannot see
   is a finding. **Must NOT duplicate** the static source-token audit — report the rendered symptom.
3. **Design-system primitives (the shared component library)** — flag **reinvented UI** the shared
   library already provides. The shared library is **`libs/web-ui`** in this repo (it is `libs/ts-ui`
   in the `ose-primer` and `ose-private` sibling repos). A bespoke button/card/input that should have
   reused a `libs/web-ui` primitive is a finding — it fragments the design language.
4. **Optional external design source** — a Figma link or mockup URL passed **at invocation**. When
   provided, `WebFetch` it and compare the live page against it; when absent, skip this source (its
   absence is never a finding).
5. **General design best-practice / visual consistency / information density ("not cramped")** —
   grounded by delegating to `web-researcher` for current design-practice references (per the
   [Web Research Delegation Convention](../../../../repo-governance/conventions/writing/web-research-delegation.md)),
   so judgements cite a principle, not a vibe.
