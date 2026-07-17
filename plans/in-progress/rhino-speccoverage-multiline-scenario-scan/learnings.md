# Learnings — Rhino speccoverage multi-line scenario scan

<!-- Knowledge Capture running log — append entries during execution. -->
<!-- Triage every entry (or record the explicit "none" escape) before archival. -->
<!-- Entry shape:
## Learning: <one-line summary>

- **Context**: what was being done when this surfaced
- **Observation**: what was noticed (sanitized — no secrets/hostnames)
- **Why it might generalize**: the litmus reasoning
-->

## Phase 0 baseline (recorded, all green)

- `npx nx run rhino-cli:test:unit` — PASS (4 features, 26 scenarios, 102 steps, all passed).
- `npx nx run rhino-cli:specs:behavior:coverage` — PASS ("Spec coverage valid! 57 specs, 316
  scenarios, 1313 steps — all covered.").
- `npx nx run web-ui:specs:behavior:coverage` — PASS ("Spec coverage valid! 21 specs, 118
  scenarios, 311 steps — all covered." — expected green since the `// prettier-ignore` hacks this
  plan removes in Phase 2 are still present).
- No preexisting failures found; nothing to resolve before Phase 1.

## Learning: Phase 3's own delivery.md commands pointed at the primary checkout, not the worktree

- **Context**: Phase 3a's sibling-propagation `cp` commands, as written verbatim in this plan's
  `delivery.md`, sourced from `/Users/wkf/ose-projects/ose-public/apps/rhino-cli/...` (the primary
  checkout, on `main`, no Phase 1/2 changes) instead of
  `/Users/wkf/ose-projects/ose-public/worktrees/rhino-speccoverage-multiline-scenario-scan/apps/rhino-cli/...`
  (the worktree where all the actual fix lives).
- **Observation**: the first copy attempt silently succeeded (cp doesn't error on stale-but-valid
  source) and only 1 of 4 new unit tests appeared in the sibling's `cargo test` run — caught
  immediately by the test count mismatch, not by a copy failure. Re-copying from the worktree path
  fixed it; `diff` then confirmed byte-identity.
- **Why it might generalize**: this is the exact same worktree-vs-primary-checkout confusion class
  already captured for Plan 1 (routed to plan-execution.md's Resume Reconciliation item 6), but this
  time the bug was baked into a plan document's own verbatim shell commands rather than an agent's
  mistaken read. Any plan template that hardcodes sibling-propagation `cp`/`diff` source paths should
  point at the worktree, not the bare repo root — worth a generalized template fix.

## Learning: touching rhino-cli marks nearly the whole Nx graph "affected," surfacing unrelated fresh-worktree provisioning gaps

- **Context**: `nx affected -t typecheck lint test:quick` in a freshly provisioned ose-primer
  worktree failed on `elixir-cabbage`, `elixir-gherkin`, `elixir-openapi-codegen`,
  `crud-be-elixir-phoenix` (missing `mix deps.get`) and `crud-be-fsharp-giraffe` (missing
  `dotnet restore`) — none of which this plan touches.
- **Observation**: because nearly every project's `specs:*`/`lint` targets shell out through the
  rhino-cli binary, any rhino-cli change marks the whole dependency graph "affected," so a fresh
  worktree's un-fetched per-language deps (Elixir Hex packages, .NET NuGet packages) surface as
  gate failures unrelated to the actual change. `npm run doctor -- --fix` does not fetch
  Elixir/`.NET` per-project dependencies.
- **Why it might generalize**: any future rhino-cli-touching plan that provisions a fresh sibling
  worktree will hit the same wall. Worth documenting in worktree-setup.md as an explicit "polyglot
  demo apps need `mix deps.get`/`dotnet restore` per-project before affected gates will pass" step,
  alongside the existing `npm install` + `npm run doctor -- --fix` guidance.
