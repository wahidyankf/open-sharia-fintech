# UI Assets — Calculator UX Hardening

This plan is **UI-bearing** (several fixes change user-facing components), but the changes are **in-place
fidelity refinements of an already-designed tool**, not new screens. The authoritative high-fidelity
design source is the originating plan's committed mockups:

- [`plans/done/2026-06-19__ayokoding-www-salary-savings-calculator/assets`](../../../done/2026-06-19__ayokoding-www-salary-savings-calculator/assets)
  — the desktop/tablet/mobile hi-fi mockups for the cost-of-living calculator. The fixes here move the
  **running page back toward** those mockups (e.g. styled select chrome, 44px controls, on-design flag).

Per the [UI Mockups in Plan Docs convention](../../../../repo-governance/conventions/formatting/diagrams/ui-mockups-principles-and-scope.md#ui-mockups-in-plan-docs-principles-in-practice-and-scope),
where a change refines an existing designed surface rather than introducing a new screen, the existing
hi-fi mockup is the target and this folder carries **Tier-1 low-fidelity** before/after wireframes for the
genuinely-visual deltas. The three with a meaningful visual decision are captured here:

- [Foreigner-school flag](./ui-foreigner-flag-low-fi.md) — wording + warning-tone styling (DWT-006 / UWT-002 / EWT-003)
- [Baseline-source segmented control at mobile](./ui-baseline-source-mobile-low-fi.md) — wrap vs stack (DWT-004)
- [Select chrome consistency](./ui-select-chrome-low-fi.md) — native arrow → styled chevron (DWT-002 / DWT-003)

Purely-semantic fixes (aria-sort, aria-pressed, aria-describedby, tooltip glosses, the tab-description
`hidden` class) and label-only changes carry **no visual layout change** and therefore need no mockup —
they are described in [tech-docs.md](../tech-docs.md) and verified by tests.

All wireframe colours below name **design-system tokens** (`bg-primary`, `text-warning`,
`text-muted-foreground`), never raw hex. Mobile, tablet, and desktop behaviour is noted where it differs.
