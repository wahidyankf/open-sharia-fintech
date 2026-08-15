# AGENTS.md

> Canonical instruction file for any AI agent or human contributor. Aligned with the
> [AGENTS.md standard](https://agents.md/).

## Repository Overview

**open-sharia-enterprise** — Sharia-compliant business platform, Nx monorepo, pre-alpha. Trunk-Based
Dev on `main`. Node.js 24 (Volta), npm. Naming: `[domain]-www` (site), `[domain]-app-web`
(client), `[domain]-be` (backend); exception `beavernest-app`.

**See**: [monorepo-structure.md](./docs/reference/monorepo-structure.md)

## Project Structure

`apps/` (deployable), `libs/` (flat), `docs/` (Diátaxis), `repo-governance/`, `plans/`, `.claude/`
(primary binding), `.opencode/` (auto-synced). Filenames: lowercase kebab-case.

**See**: [add-new-app.md](./docs/how-to/add-new-app.md)

## Build, Test, Lint

```bash
npm install                     # deps + doctor
nx run [project]:test:quick     # pre-push gate
nx affected -t build,test:quick,lint
npm run doctor -- --fix
```

**See**: [nx-targets.md](./repo-governance/development/infra/nx-targets.md)

## Quality Gates

Markdown auto-linted via hooks/CI. Cross-language lint at warning-and-above. Instruction files carry
a word budget; READMEs need annotated indexes; remediation is progressive disclosure.

**See**: [governance-word-budget.md](./repo-governance/conventions/structure/governance-word-budget.md),
[governance-readme-completeness.md](./repo-governance/conventions/structure/governance-readme-completeness.md)

## Git Workflow

`main` is the sole integration target; `prod-*`/`stag-*` deploy targets, never committed
directly. Conventional Commits, imperative, no period. After a rebase/pull/merge lands foreign
commits, read the full diff first.

**See**: [commit-messages.md](./repo-governance/development/workflow/commit-messages.md)

### Delivery Mode

`worktree-to-pr` is mandatory. Executable work runs CI-gated review cycles; static work needs a
green `pr-quality-gate.yml`. `[AI]` merges by default. One worktree per repo per plan; Phase 0 opens
none.

**See**: [Delivery Mode](./repo-governance/conventions/structure/plans/32-delivery-mode-the-four-modes.md#delivery-mode)

## Conventions

Deliberate Problem-Solving, Simplicity Over Complexity, Root Cause Orientation, Accessibility
First, No Time Estimates. TDD required. Specs & Gherkin required for code changes. Every bug fix
carries a regression test; every plan ends with Knowledge Capture.

**See**: [Principles Index](./repo-governance/principles/README.md)

### Reproducible Environments

Never commit secrets. Real values live only in uncommitted `.env*` (except `.env.example`); agents
must not touch `.env.prod`/`.env.stag`. No agent sets/modifies git identity.

**See**: [Secrets and Env Standards](./repo-governance/conventions/security/secrets-and-env-standards.md)

### Agent Workflow Orchestration

Plan mode for non-trivial tasks. N+1 model (1 main + N background, default N=3). File-touch ledger
reconciled against `git status`. Harness sync generated (`.claude/` hand-authored; others via
`npm run generate:bindings`, same commit). Poll CI every 2 minutes, never `gh run watch`.

**See**: [agent-workflow-orchestration.md](./repo-governance/development/agents/agent-workflow-orchestration.md)

## Manual Verification & CI Blockers

Verify UI/API behavior manually; investigate CI failures at the root cause, never bypass.

**See**: [ci-blocker-resolution.md](./repo-governance/development/quality/ci-blocker-resolution.md)

## AI Agents

[Agent catalog](./.claude/agents/README.md) is authoritative, `<domain>-<role>` naming.
maker/checker/fixer pattern. PR Review Cycle: nine specialists → `pr-review-synthesis-maker` →
`pr-review-fixer`. Skills at `.claude/skills/<name>/SKILL.md`.

**See**: [ai-agents.md](./repo-governance/development/agents/ai-agents.md)

## Repository Architecture

Six-layer: Vision → Principles → Conventions → Development → AI Agents → Workflows.

**See**: [repository-governance-architecture.md](./repo-governance/repository-governance-architecture.md)

## Web Sites

Names, domains, ports, and prod branches for every app.

**See**: [Web Sites reference](./docs/reference/web-sites.md)

## Plans & Temporary Files

`plans/`: `ideas/`, `backlog/`, `in-progress/`, `done/`. `generated-reports/`, `local-temp/`. Build
artifacts may be swept at any time — regenerate, never protect.

**See**: [plans.md](./repo-governance/conventions/structure/plans.md)

## Important Notes

Do NOT stage/commit unless explicitly instructed. License MIT — see
[LICENSING-NOTICE.md](./LICENSING-NOTICE.md).

## Related Repositories

Three sibling repos: [ose-public](https://github.com/wahidyankf/ose-public) (this repo, upstream),
[ose-primer](https://github.com/wahidyankf/ose-primer) (template),
[ose-private](https://github.com/wahidyankf/ose-private) (infra). `apps/rhino-cli` byte-identity
spans all three.

**See**: [Related Repositories reference](./docs/reference/related-repositories.md)

## Platform Binding Examples

Vendor-specific; the audit scanner skips this section. Tier-1 harnesses read `AGENTS.md` natively.
Exceptions: Claude Code → `.claude/`; OpenCode → `.opencode/agents/`; Cursor → `.cursor/agents/`;
Amazon Q → `.amazonq/`; Aider → `CONVENTIONS.md`. Mirrors generated via
`rhino-cli harness bindings generate`.

**See**: [platform catalog](./docs/reference/platform-bindings.md)
