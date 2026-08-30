# Inputs

The orchestrator (or user) provides:

1. **URL(s)** — one or more live targets (required). Production, staging, preview, or a local dev
   server (e.g. `http://localhost:3200/...`).
2. **Design goal** — the evaluation mission (required). Examples: "verify the pricing page matches the
   mockups and design tokens across breakpoints", "audit the dashboard for design-system-primitive
   reuse and spacing discipline", "check the landing page against this Figma frame".
3. **Optional refinements**:
   - **External design source** — a Figma link or a mockup URL to compare against, passed at
     invocation. When provided, the agent fetches it (`WebFetch`) and compares the live page to it;
     when absent, this source is skipped (its absence is never itself a finding).
   - **Breakpoints** — viewport widths to test. Default mobile/tablet/desktop = **375, 768, 1280**
     (plus 320 for the small-phone reflow check and 1440 for wide desktop when depth is `thorough`).
   - **Locales** — language variants to evaluate. **Default and minimum: ALL locales the target
     supports** — discover them from the app's i18n config (`apps/<target>/src/features/i18n/` or
     `next.config.ts`) or from the locale-prefixed routes (`/en/`, `/id/`). Evaluating only the default
     locale is INCOMPLETE: text length, line wrapping, and density differ per language, so every visual
     pass runs against every supported locale, and the coverage map records which locales were
     exercised.
   - **Depth** — `quick` (one route, mockup + token pass at desktop), `standard` (default; full
     five-source sweep across breakpoints/locales), or `thorough` (adds external-source diffing, deep
     design-practice research, and a cross-surface consistency audit).
   - **Ground-truth pointers** — a plan folder, `assets/` mockups, or design-token/theme files to test
     the live page against. Even when none are named, the agent reads the plan `assets/` mockups and the
     design tokens/theme by default — see _The Five Ground-Truth Sources_.
4. **Output mode & destination** — `local-tmp` (default) | `plan` | `delivery`; `plan` and
   `delivery` require explicit selection and destination; see _Output Modes_.
   With `delivery`, also pass a **plan-path** (the existing plan whose `delivery.md` receives the
   findings); with `plan`, optionally pass `plan-stage: in-progress` to file directly into
   `plans/in-progress/`.

If the goal or URL is missing, ask for it before evaluating — do not invent a target.
