# AGENTS.md

> Canonical instructions for agents and contributors, aligned with the
> [AGENTS.md standard](https://agents.md/).

## Repository Overview

**open-sharia-enterprise** — Sharia-compliant Nx monorepo, pre-alpha.
Trunk-Based Dev on `main`. Node.js 24 (Volta), npm.

**See**: [monorepo-structure.md](./docs/reference/monorepo-structure.md) (app naming),
[web-sites.md](./docs/reference/web-sites.md) (domains, ports)

## Glossary

Terms are repository-wide.

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
rtk npm install                     # deps + doctor
rtk nx run [project]:test:quick     # pre-push gate
rtk nx affected -t build,test:quick,lint
```

**See**: [nx-targets.md](./repo-governance/development/infra/nx-targets.md)

## Quality Gates

Markdown auto-linted via hooks/CI; cross-language lint at warning-and-above. Instruction files carry
a word budget; READMEs need annotated indexes.

**See**: [governance-word-budget.md](./repo-governance/conventions/structure/governance-word-budget.md),
[governance-readme-completeness.md](./repo-governance/conventions/structure/governance-readme-completeness.md)

## Git Workflow

`main` is the sole integration target; never commit directly to `prod-*`/`stag-*`. Conventional
Commits: imperative, no period. After new commits land, read their full diff; reconcile task, plan,
assumptions, ledger, and verification before acting.

**See**: [commit-messages.md](./repo-governance/development/workflow/commit-messages.md)

### Delivery Mode

`worktree-to-pr` is mandatory. Executable work and `plans/**` run review cycles plus
`pr-quality-gate.yml`; other static work, the gate only. `[AI]` merges by default. One worktree per repo per plan; Phase 0 opens
none.

**See**: [Delivery Mode](./repo-governance/conventions/structure/plans/delivery-mode-the-four-modes.md#delivery-mode)

## Conventions

Follow the [Principles Index](./repo-governance/principles/README.md). Code changes require TDD and
Specs/Gherkin; bug fixes require regression tests. Plans end with Knowledge Capture. PR bodies
state new-code cost/benefit; tests exempt.

Use English for repository-authored material and developer-facing source text; declared localized
content and user-facing values are exempt. See [Working Language](./repo-governance/conventions/writing/repository-working-language.md).

### Reproducible Environments

Never commit secrets; real values only in uncommitted `.env*` (except `.env.example`). Never touch
`.env.prod`/`.env.stag`. No agent sets or modifies git identity.

**See**: [Secrets and Env Standards](./repo-governance/conventions/security/secrets-and-env-standards.md)

### Agent Workflow Orchestration

Maintain task list. Plan non-trivial work. Preserve
user-set rules across compaction/handoff; reconcile before resuming. N+1 agents (N=3). Reconcile the
file ledger with `git status`. Hand-author `.claude/`; generate mirrors together. New worktree: run
`rtk npm install` at its root. Poll CI every 2
minutes; never `gh run watch`. If main only polls non-CI background work, update user every 5 minutes.

**See**: [agent-workflow-orchestration.md](./repo-governance/development/agents/agent-workflow-orchestration.md)

## Manual Verification & CI Blockers

Verify UI/API behavior manually; investigate CI failures at the root cause, never bypass.

**See**: [ci-blocker-resolution.md](./repo-governance/development/quality/ci-blocker-resolution.md)

## AI Agents

[Agent catalog](./.claude/agents/README.md) is authoritative; filenames follow the ordinary
kebab-case rule. Agent skills at `.claude/skills/<name>/SKILL.md`, mirrored to `.agents/skills/`.

**See**: [ai-agents.md](./repo-governance/development/agents/ai-agents.md)

## Plans & Temporary Files

Regenerate swept `generated-reports/` and `local-tmp/` artifacts; never protect.

**See**: [plans.md](./repo-governance/conventions/structure/plans.md)

## Important Notes

Stage/commit only when explicitly instructed. License MIT — see
[LICENSING-NOTICE.md](./LICENSING-NOTICE.md).

## Related Repositories

Sole parity sibling: [ose-private](https://github.com/wahidyankf/ose-private); `apps/rhino-cli` byte-identical.
Independent/family-only: [BeaverNest](https://github.com/wahidyankf/beaver-nest); work stays there; learnings inform OSE.

[Details](./docs/reference/related-repositories.md)

## Platform Binding Examples

Vendor-specific; audits skip this section. `repo-config.yml` `harness:` is authoritative.

**See**: [platform catalog](./docs/reference/platform-bindings.md)

@RTK.md
