---
description: "Rules 7-10: green gates insufficient, theme-token colors, per-breakpoint responsive, done means verified."
when_to_use: "Use when authoring or verifying a UI plan against rules 7-10."
---

# The Sixteen Rules (7-10)

1. **(Authoring) Green automated gates are necessary, not sufficient, for UI/UX correctness.** Gap:
   four real defects plus a label-clarity issue shipped with unit/E2E/lint/typecheck/CI all green.
   Apply: the maker-checker-fixer loop for UI work needs a human-or-Playwright visual sign-off rung
   the automated gates cannot substitute for.

2. **(Authoring) Mockup colors MUST be specified as theme tokens, then reconciled to the app's
   brand.** Gap: the mockups used a generic palette; the first implementation copied raw colors
   (teal) that were off-brand for the target app and mis-mapped a semantic badge. Apply: plan-doc
   mockups annotate each color with the **theme token** it represents (`active = --color-primary`,
   `covered = hue=sage`), not a raw swatch; the delivery step reconciles to the specific app's brand
   tokens; `plan-checker` flags raw-value colors with no token mapping.

3. **(Execution) Responsive is per-breakpoint work, not a CSS afterthought.** Technique: the
   **dual-render pattern** — one computed dataset, two DOM views (table + cards) toggled by Tailwind
   `md:`/`lg:`; tablet hides granular columns via `hidden lg:table-cell`; mobile renders stacked
   cards. Keep the canonical test-ids on a single view so assertions stay unambiguous. Verify at
   each viewport with Playwright.

4. **(Verification) "Zero findings + CI green" is NOT "done" — and definitely not "archive" — for
   a user-facing change.** Gap: the plan was validated to zero findings and archived to
   `plans/done/` while the UI was bland and off-design. Apply: the done/archival criterion for any
   user-facing change includes a **production visual sign-off against the mockups, per breakpoint,
   per locale**; plan-execution finalization blocks archival until that sign-off is recorded. The
   sign-off MUST cover ALL supported locales (not just the default locale) and MUST be evidenced by
   committed screenshots in `evidence/` with paths referenced in `delivery.md`. Discovering after
   archival that only one locale was tested is a Rule 14 reopen event.
