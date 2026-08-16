# Instruction-File Size-Budget Gate

**Status**: In Progress
**Created**: 2026-06-26
**Authored in**: `ose-public` (this repo)
**Type**: Multi-file plan (5 documents) — **comprehensive 3-repo plan** (`ose-public` →
Phases 0–6, `ose-primer` → Phase 7, `ose-infra` → Phase 8, cross-repo verify → Phase 9)

> Generalizes the existing single-file `rhino-cli convention agents-md-size` gate into a
> **multi-file instruction-file size budget** covering the whole "AGENTS.md-class" of
> auto-loaded instruction surfaces, recalibrates the thresholds to the real per-harness
> limits, **forces the gate at pre-push when those files change**, also enforces it in the
> **PR quality gate**, emits it as a **deterministic preflight category** so `repo-rules-checker`
> and the `repo-rules-quality-gate` workflow track it without AI byte-counting, trims
> `AGENTS.md` back under budget, names **progressive disclosure** as the sanctioned remediation,
> and formalizes the rule as a governance convention propagated by `repo-rules-maker`. The same
> change lands across **all three sibling repos** (`ose-public`, `ose-primer`, `ose-infra`).

## Context

A Claude Code runtime warning fired: the resolved `CLAUDE.md` tree (`CLAUDE.md` +
`@AGENTS.md` import) exceeds **40,000 characters**. Root cause: `AGENTS.md` is **41,108
bytes** — it inline-expands governance content that already lives behind links in
`repo-governance/`.

A deterministic gate already exists — `rhino-cli convention agents-md-size`
(source: `apps/rhino-cli/src/application/repo_governance/agents_md_size.rs`, deleted after this
plan was superseded by the word-budget gate) — but it has three gaps:

1. **Single file only.** It measures `AGENTS.md` and nothing else. The repo is
   multi-harness (Claude Code, OpenCode, Codex CLI, Copilot, Cursor, Windsurf, Junie,
   Amazon Q, Aider) and each harness auto-loads its own instruction surface. Those are
   unguarded.
2. **Thresholds are too loose.** Its hard limit is 40,000 bytes — but OpenAI Codex CLI
   **silently truncates `AGENTS.md` at 32,768 bytes** (`project_doc_max_bytes`), and an
   `AGENTS.md` near 40k pushes the Claude resolved tree well past the 40k warning. Codex
   users are **already losing the bottom ~8k bytes of `AGENTS.md`** with no warning.
3. **Not enforced at pre-push.** It is referenced as a pre-commit/CI gate but is not wired
   into `.husky/pre-push`, so an over-budget instruction file can be pushed.

## Scope

**In scope** (all three repos — `ose-public`, `ose-primer`, `ose-infra`):

- Generalize `convention agents-md-size` → a config-driven, multi-file
  `convention instruction-size` validator (keep `agents-md-size` as a thin alias).
- A committed **per-file size-budget config** (`instruction-size-budget.yaml`) with
  per-surface `target` / `warn` / `fail` byte thresholds — see
  [tech-docs §2](./tech-docs.md#2-per-file-size-budget-the-numbers).
- A **Claude resolved-tree** check (`CLAUDE.md` + recursive `@imports`) against the 40k
  runtime-warning ceiling.
- **Pre-push enforcement**, changed-path-gated to the instruction-file globs (mirrors the
  existing naming/parity gates in `.husky/pre-push`); **PR quality gate** enforcement in
  `commons-quality-gate.yml`; pre-commit early-catch.
- A **deterministic preflight category** (`instruction-size` added to `repo-governance audit`)
  so `repo-rules-checker` and the `repo-rules-quality-gate` workflow consume the finding from
  the JSON envelope — **no AI byte-counting**.
- **Progressive disclosure** named as the one sanctioned remediation (surfaced in the gate's
  `fail` message, the convention, and the checker), forbidding the three anti-fixes.
- **Fix the existing violation in each repo**: trim each repo's over-budget `AGENTS.md` under
  the new ceiling (by progressive disclosure) so no repo ships a gate it currently fails.
- A new **governance convention** authored by `repo-rules-maker`, propagated across all
  surfaces, with a two-way backlink to the Progressive Disclosure principle.
- Deterministic integration into **`repo-rules-checker` Step 0.5 + Step 6** and
  **`repo-rules-quality-gate.md`**; companion **`specs/apps/rhino`** Gherkin + `specs:coverage`.

**Execution model**: `ose-public` first (in a worktree → commit + push to `origin/main`), then
`ose-primer` and `ose-infra` **in parallel**, then cross-repo parity verification + archival.

**Out of scope**:

- Authoring `.cursor/rules`, `.windsurf/rules`, `.github/copilot-instructions.md`,
  `CONVENTIONS.md` — the budget covers them **if/when added**; their globs are no-ops until
  the files exist.

## Approach Summary

**Part A — `ose-public`** (worktree → push to `main`):

- **Phase 0** — worktree + baseline (`repo-setup-manager`); capture current sizes.
- **Phase 1** — budget config + generalized Rust validator (TDD) + resolved-tree check +
  deterministic preflight category.
- **Phase 2** — wire the `instruction-size:validation` Nx target into pre-push
  (changed-path-gated), pre-commit, and the PR quality gate.
- **Phase 3** — fix the existing violation: trim `AGENTS.md` under the ceiling.
- **Phase 4** — author the governance convention (`repo-rules-maker`) + propagate + principle
  backlink.
- **Phase 5** — deterministic integration into `repo-rules-checker` Step 0.5 + Step 6 and
  `repo-rules-quality-gate.md`; companion specs + `specs:coverage`.
- **Phase 6** — verify + commit + push to `ose-public` `origin/main`; remove worktree.

**Part B — `ose-primer` + `ose-infra`** (in parallel, after Part A lands):

- **Phase 7** — propagate to `ose-primer` (own sub-steps; fixes its own `AGENTS.md`).
- **Phase 8** — propagate to `ose-infra` (bare repo + worktree; fixes its own `AGENTS.md`).

**Part C:**

- **Phase 9** — cross-repo parity verification + archival.

## Navigation

- [brd.md](./brd.md) — why this matters (business rationale)
- [prd.md](./prd.md) — what "done" looks like (personas, user stories, Gherkin acceptance criteria)
- [tech-docs.md](./tech-docs.md) — the monitored file class, the budget numbers + rationale, validator design, wiring, and diagrams
- [delivery.md](./delivery.md) — the phased, TDD-shaped execution checklist

## Related

- `apps/rhino-cli/src/application/repo_governance/agents_md_size.rs` — the single-file gate this plan generalized; since deleted, so no link resolves
- [.husky/pre-push](../../../.husky/pre-push) — the changed-path-gated hook this plan extends
- [repo-rules-quality-gate workflow](../../../repo-governance/workflows/repo/repo-rules-quality-gate.md) — Step 6 / preflight integration
- [.claude/agents/repo-rules-checker.md](../../../.claude/agents/repo/repo-rules-checker.md) — Step 6 "AGENTS.md Size Check" being extended
- [repo-governance/development/infra/nx-targets.md](../../../repo-governance/development/infra/nx-targets.md) — canonical Nx target names
