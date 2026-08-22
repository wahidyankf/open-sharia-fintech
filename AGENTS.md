# AGENTS.md

> Canonical instruction file for any AI agent or human contributor. Aligned with the
> [AGENTS.md standard](https://agents.md/).

## Repository Overview

**open-sharia-enterprise** — Sharia-compliant business platform, Nx monorepo, pre-alpha.
Trunk-Based Dev on `main`. Node.js 24 (Volta), npm.

**See**: [monorepo-structure.md](./docs/reference/monorepo-structure.md) (app naming),
[web-sites.md](./docs/reference/web-sites.md) (domains, ports)

## Glossary

These terms carry exactly these meanings everywhere.

- **Repo rules** — every normative surface, not one directory: `repo-governance/`, `AGENTS.md`,
  `CLAUDE.md`, `.claude/` + mirrors, `repo-config.yml`, enforcement machinery, SE style guides.
- **Content trees** — `docs/` explains, `repo-governance/` binds, `plans/` expires, `specs/` tests.
- **Delivery unit** — one branch, one PR, one shippable slice; phases are smaller.
- **Surface** — what a gate measures; **binding** — a harness mirror.

**See**: [glossary.md](./repo-governance/glossary.md)

## Project Structure

`apps/` (deployable), `libs/` (flat), `.claude/` (primary binding), `.opencode/` (auto-synced).
Filenames: lowercase kebab-case.

**See**: [add-new-app.md](./docs/how-to/add-new-app.md),
[repository-governance-architecture.md](./repo-governance/repository-governance-architecture.md)

## Build, Test, Lint

```bash
npm install                     # deps + doctor
nx run [project]:test:quick     # pre-push gate
nx affected -t build,test:quick,lint
```

**See**: [nx-targets.md](./repo-governance/development/infra/nx-targets.md)

## Quality Gates

Markdown auto-linted via hooks/CI; cross-language lint at warning-and-above. Instruction files carry
a word budget; READMEs need annotated indexes.

**See**: [governance-word-budget.md](./repo-governance/conventions/structure/governance-word-budget.md),
[governance-readme-completeness.md](./repo-governance/conventions/structure/governance-readme-completeness.md)

## Git Workflow

`main` is the sole integration target; `prod-*`/`stag-*` deploy targets, never committed
directly. Conventional Commits, imperative, no period. After a rebase/pull/merge lands foreign
commits, read the full diff first.

**See**: [commit-messages.md](./repo-governance/development/workflow/commit-messages.md)

### Delivery Mode

`worktree-to-pr` is mandatory. Executable work and `plans/**` run review cycles plus
`pr-quality-gate.yml`; other static work, the gate only. `[AI]` merges by default. One worktree per repo per plan; Phase 0 opens
none.

**See**: [Delivery Mode](./repo-governance/conventions/structure/plans/delivery-mode-the-four-modes.md#delivery-mode)

## Conventions

Deliberate Problem-Solving, Simplicity Over Complexity, Root Cause Orientation, Accessibility
First, No Time Estimates. TDD required. Specs & Gherkin required for code changes. Every bug fix
carries a regression test; every plan ends with Knowledge Capture. New code states its
cost/benefit in the PR body; tests exempt.

**See**: [Principles Index](./repo-governance/principles/README.md)

### Reproducible Environments

Never commit secrets; real values only in uncommitted `.env*` (except `.env.example`). Never touch
`.env.prod`/`.env.stag`. No agent sets or modifies git identity.

**See**: [Secrets and Env Standards](./repo-governance/conventions/security/secrets-and-env-standards.md)

### Agent Workflow Orchestration

Open the harness-native task list before any task, conversational included; keep it live. Plan
mode for non-trivial tasks. N+1 agents (default N=3). File-touch ledger reconciled against
`git status`. `.claude/` hand-authored; mirrors via `npm run generate:bindings`, same commit. Poll
CI every 2 minutes, never `gh run watch`.

**See**: [agent-workflow-orchestration.md](./repo-governance/development/agents/agent-workflow-orchestration.md)

## Manual Verification & CI Blockers

Verify UI/API behavior manually; investigate CI failures at the root cause, never bypass.

**See**: [ci-blocker-resolution.md](./repo-governance/development/quality/ci-blocker-resolution.md)

## AI Agents

[Agent catalog](./.claude/agents/README.md) is authoritative; filenames follow the ordinary
kebab-case rule. Agent skills at `.claude/skills/<name>/SKILL.md`, mirrored to `.agents/skills/`.

**See**: [ai-agents.md](./repo-governance/development/agents/ai-agents.md)

## Plans & Temporary Files

Build artifacts in `generated-reports/` and `local-tmp/` may be swept at any time — regenerate,
never protect.

**See**: [plans.md](./repo-governance/conventions/structure/plans.md)

## Important Notes

Do NOT stage/commit unless explicitly instructed. License MIT — see
[LICENSING-NOTICE.md](./LICENSING-NOTICE.md).

## Related Repositories

Sole parity sibling: [ose-private](https://github.com/wahidyankf/ose-private) (infra).
`apps/rhino-cli` byte-identity spans both.

**See**: [Related Repositories reference](./docs/reference/related-repositories.md)

## Platform Binding Examples

Vendor-specific; the audit scanner skips this section. `repo-config.yml` `harness:` is authoritative.

**See**: [platform catalog](./docs/reference/platform-bindings.md)
