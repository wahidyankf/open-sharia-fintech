# Plan: web-ui Code-Block Copy Button

Add a one-click **copy-to-clipboard** affordance to every rendered fenced code block in
`apps/ayokoding-www` and `apps/ose-www`, built as a **reusable `libs/web-ui` primitive** so the same
capability is available to any app. The copy reproduces the **verbatim fenced source** — including the
heavily-annotated `--` comments and `-- => output` markers authors write literally in the fence — not
the syntax-highlighted DOM decorations.

## Problem in One Line

Readers of AyoKoding's densely-annotated worked examples (and future OSE code content) cannot copy a
snippet without hand-selecting across syntax-highlight spans, losing whitespace, or accidentally
grabbing line numbers; a positioned Copy button removes that friction across both sites from one shared
component.

## Delivery Mode

`worktree-to-pr`, with an explicit **maintainer-directed merge deviation**. Work happens in
`worktrees/web-ui-code-block-copy-button/` on a feature branch and lands via a **draft PR**. The
`worktree-to-pr` default is a `[HUMAN]` merge; for this plan the maintainer authorized the **AI to merge
the PR itself** once (a) the 3-cycle `pr-review-maker` → `pr-review-fixer` loop has completed and (b) all
local quality gates and CI are green — **no human merge wait**. This matches the maintainer's established
practice on the recent ayokoding plans; it is a per-plan authorization, not a new codified Delivery Mode.
The `plans/done/` archival is folded into the PR before the merge; after the merge the AI verifies `main`
CI is green, then **deploys both apps to production** via their deployer agents.

See [`delivery.md`](./delivery.md) for the full mode declaration, the PR-review cycle, and the two prod
deploys.

## Scope

**In scope**

- New `libs/web-ui` primitive family under `src/primitives/code-block/`: `CopyButton` (standalone),
  `CodeBlock` (layout composer), and a colocated `useCopyToClipboard` hook — with unit tests, Gherkin
  step tests, accessibility (axe) assertions, Storybook stories, and Playwright visual baselines.
- Wire `CodeBlock` into `apps/ayokoding-www`'s markdown renderer (bilingual en/id labels) with a real
  end-to-end proof against an existing annotated code block.
- Wire `CodeBlock` into `apps/ose-www`'s markdown renderer as **latent wiring** (unit-tested replace
  logic only — ose-www currently has zero non-mermaid code blocks, so no live e2e).
- Deploy both apps to production.

**Out of scope**

- Inline code (single backticks) — untouched.
- Mermaid fenced blocks — explicitly excluded (they render as diagrams).
- Authoring new marketing/code content for ose-www.
- Any `package.json` dependency change (apps consume web-ui via the existing tsconfig path alias).

## Documents

| Doc                              | Purpose                                                                                      |
| -------------------------------- | -------------------------------------------------------------------------------------------- |
| [`brd.md`](./brd.md)             | WHY — business rationale, impact, affected roles, success signals, risks                     |
| [`prd.md`](./prd.md)             | WHAT — product overview, personas, user stories, Gherkin acceptance criteria                 |
| [`tech-docs.md`](./tech-docs.md) | HOW — component API, injection strategy, i18n, CSS/positioning, a11y, clipboard, **mockups** |
| [`delivery.md`](./delivery.md)   | Executable phased checklist (Phase 0 → web-ui → ayokoding → ose-www → PR/merge → deploy)     |
| [`learnings.md`](./learnings.md) | Running knowledge-capture log, triaged in the final phase                                    |

**UI design** — the full funnel (low-fi alternatives + rationale + the two committed high-fidelity
finalists, light + dark, in context) lives in [`prd.md` § UI Design Funnel](./prd.md#ui-design-funnel);
the token/anatomy spec behind the finalists is in
[`tech-docs.md` § Hi-Fi Token Spec & Anatomy](./tech-docs.md#hi-fi-token-spec--anatomy). An interactive,
theme-toggleable review copy is at <https://claude.ai/code/artifact/9cf28211-fb93-4eaa-ac3f-4aecca818be9>.

## Worktree

See [`delivery.md` § Worktree](./delivery.md#worktree).
