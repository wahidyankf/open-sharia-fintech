# AGENTS.md

> Canonical instruction file for any AI coding agent or human contributor working in this repo.
> Aligned with the [AGENTS.md standard](https://agents.md/) (Agentic AI Foundation / Linux Foundation).

## Repository Overview

**open-sharia-enterprise** — Enterprise platform for Sharia-compliant business systems, Nx monorepo.

**Status**: Phase 1 (OrganicLever — Productivity Tracker)
**License**: MIT
**Main Branch**: `main` (Trunk Based Development)

### Tech Stack

- **Node.js**: 24.13.1 (LTS, managed by Volta)
- **npm**: 11.10.1
- **Monorepo**: Nx workspace
- **App naming tiers**: `[domain]-www` = public website at the domain root; `[domain]-app-web` = product
  web client at `app.*`; `[domain]-be` = generic HTTP backend for a product domain.
- **Current Apps**: Next.js sites, F# backends, Rust and F# CLIs, a contract spec, and paired E2E
  suites — names and ports in the Web Sites table below and in
  [monorepo structure](./docs/reference/monorepo-structure.md).

Polyglot demo apps extracted 2026-04-18 to [`ose-primer`](https://github.com/wahidyankf/ose-primer)
(now authoritative for the polyglot showcase).

## Project Structure

`apps/` (Nx apps), `libs/` (`rust-commons`, `fsharp-crane-core`, `web-ui`), `docs/` (Diátaxis:
tutorials/how-to/reference/explanation), `repo-governance/`
(conventions/development/principles/workflows/vision), `plans/` (backlog/in-progress/done), `.claude/`
(primary binding: agents + skills), `.opencode/` (auto-synced from `.claude/`).

**See**: [docs/reference/monorepo-structure.md](./docs/reference/monorepo-structure.md)

## Build, Test, Lint Commands

```bash
npm install                           # Install deps (runs doctor)
nx build [project]                    # Build
nx run [project]:test:quick           # Pre-push quality gate
nx run [project]:test:unit            # Unit (cacheable)
nx run [project]:test:integration     # Integration (NOT cacheable)
nx run [project]:test:e2e             # E2E (NOT cacheable)
nx affected -t build,test:quick,lint  # Affected projects only
nx graph                              # Dependency graph
npm run doctor -- --fix               # Install missing tools
npm run lint:md:fix                   # Fix markdown violations
```

**Worktree setup**: After `git worktree add`, run `npm install` AND `npm run doctor -- --fix`. See
[Worktree Toolchain Initialization](./repo-governance/development/workflow/worktree-setup.md).

**See**: [repo-governance/development/infra/nx-targets.md](./repo-governance/development/infra/nx-targets.md)
for canonical target names, coverage thresholds, caching rules, and the three-level testing standard.

## Markdown Quality

All markdown auto-linted via Prettier (pre-commit), markdownlint-cli2 (pre-push), and rhino-cli's
`md mermaid validate`, `md links validate`, and `md heading-hierarchy validate` subcommands (wired
into pre-commit/pre-push hooks and CI as raw `cargo run` invocations — not Nx targets). Quick fix:
`npm run lint:md:fix`.

**See**: [repo-governance/development/quality/markdown.md](./repo-governance/development/quality/markdown.md),
[repo-governance/development/quality/repository-validation.md](./repo-governance/development/quality/repository-validation.md)

## Cross-Language Lint Gates

Shell scripts, Dockerfiles, GitHub Actions, and F# gated at **warning-and-above** (CI + Husky hooks).
Linters: shellcheck (`--severity=warning`), hadolint (`--failure-threshold warning`), actionlint,
F# strict (`TreatWarningsAsErrors` + G-Research.FSharp.Analyzers + `fantomas --check`).
All installed by `npm run doctor -- --fix`.

**Instruction-file size budget** (`nx run rhino-cli:instruction-size:validation`): per-surface byte
thresholds on auto-loaded instruction files; sole remediation is progressive disclosure.
See [Instruction-File Size Budget Convention](./repo-governance/conventions/structure/instruction-file-size-budget.md).

**See**: [repo-governance/development/quality/cross-language-lint-strictness.md](./repo-governance/development/quality/cross-language-lint-strictness.md)

## Monorepo Architecture

`apps/` — deployable, naming `[domain]-[type]`, import libs but never export, never import other apps.
`libs/` — flat, naming `ts-[name]`/`rust-[name]`/`fsharp-[name]`, import via
`@open-sharia-enterprise/ts-[lib-name]`, no circular deps.

**See**: [docs/reference/monorepo-structure.md](./docs/reference/monorepo-structure.md),
[docs/how-to/add-new-app.md](./docs/how-to/add-new-app.md),
[repo-governance/development/infra/nx-targets.md](./repo-governance/development/infra/nx-targets.md)

## Git Workflow

**Trunk Based Development** — `main` is the single integration target. Every `prod-*` and `stag-*`
ref is a deploy target — **never commit directly**. `git branch -r` is authoritative and includes
lib/backend targets (`prod-web-ui`, `stag-ose-be`) absent from the Web Sites table below.
**Commit format**: Conventional Commits `<type>(<scope>): <description>` — imperative mood, no
period. Split by domain/concern.

**See**: [repo-governance/development/workflow/commit-messages.md](./repo-governance/development/workflow/commit-messages.md)

### Worktree Path

Worktrees land at **`worktrees/<name>/`** in the repo root (gitignored). Routing handled by a
repo-local `WorktreeCreate` hook.

**See**: [repo-governance/conventions/structure/worktree-path.md](./repo-governance/conventions/structure/worktree-path.md)

### Delivery Mode

Every plan declares exactly one of four Delivery Modes controlling where it's worked and how it
lands: `worktree-to-pr` (worktree → draft PR — **the default**), `worktree-to-origin-main` (worktree
→ direct push), `main-to-origin-main` (primary checkout → direct push), `main-to-pr` (primary
checkout → draft PR). `*-to-pr` modes run the **PR-Review Maker→Fixer Cycle** (`pr-review-maker` /
`pr-review-fixer`, default 3 sequential CI-gated cycles) before the merge. **`[AI]` merges by
default** in every mode; a `[HUMAN]` merge gate applies only where a plan's own step says so
explicitly, with identical preconditions — only the actor differs.

**The PR is the independent merge point** — N parallel units become N PRs that review, gate, and
merge independently, which is why `worktree-to-pr` is the default; each DAG leaf producing changes
gets its own worktree and PR (strict 1-PR ↔ 1-worktree), while genuinely dependent nodes stay one PR.
A PR merges only when **all five hardened preconditions** hold — review cycles complete; 0 CRITICAL +
0 HIGH outstanding; branch non-destructively up to date with `origin/main`; all quality gates green;
tester gates run or exemption recorded. Normative lettering (a)-(e) in the PR Merge Protocol.

**See**: [PR Merge Protocol](./repo-governance/development/workflow/pr-merge-protocol.md),
[Plans Organization Convention §Delivery Mode](./repo-governance/conventions/structure/plans.md#delivery-mode),
[PR Review Quality Gate workflow](./repo-governance/workflows/pr/pr-review-quality-gate.md)

## Git Hooks (Automated Quality)

Pre-commit: format (Prettier/gofmt/rustfmt), validate markdown links + markdownlint, lint
shell/Dockerfiles/workflows, auto-sync platform bindings, auto-stage. Commit-msg: Commitlint.
Pre-push: `typecheck`, `lint`, `test:quick`, `specs:coverage` for affected projects (parallelism:
cores-1); markdown linting. All four Nx targets cacheable — warm cache before push if timeout occurs.

**See**: [repo-governance/development/quality/code.md](./repo-governance/development/quality/code.md)

## Documentation Organization

**Diátaxis Framework**: `docs/tutorials/` (learning), `docs/how-to/` (problem-solving),
`docs/reference/` (specs), `docs/explanation/` (concepts). File naming: lowercase kebab-case;
exception: `README.md`.

**See**: [repo-governance/conventions/structure/file-naming.md](./repo-governance/conventions/structure/file-naming.md),
[repo-governance/conventions/structure/diataxis-framework.md](./repo-governance/conventions/structure/diataxis-framework.md)

## Conventions

Core principles (see [Principles Index](./repo-governance/principles/README.md) for full list):

- **Deliberate Problem-Solving**: Understand before acting; prefer reversible decisions
- **Simplicity Over Complexity**: Minimum viable abstraction
- **Root Cause Orientation**: Fix root causes, not symptoms; proactively fix preexisting errors
  encountered during work (do not mention and defer)
- **Accessibility First**: WCAG AA compliance, color-blind friendly
- **No Time Estimates**: Never give time estimates; focus on outcomes

### File Naming

Lowercase kebab-case (`[a-z0-9-]+`). Exception: `README.md`, `docs/metadata/` files.

**See**: [repo-governance/conventions/structure/file-naming.md](./repo-governance/conventions/structure/file-naming.md)

### Linking

GitHub-compatible markdown with `.md` extension.

**See**: [repo-governance/conventions/formatting/linking.md](./repo-governance/conventions/formatting/linking.md)

### Indentation

Markdown nested bullets: 2 spaces. YAML frontmatter: 2 spaces. Code: language-specific.

**See**: [repo-governance/conventions/formatting/indentation.md](./repo-governance/conventions/formatting/indentation.md)

### Emoji Usage

Allowed: `docs/`, README, `plans/`, `repo-governance/`, `AGENTS.md`, `CLAUDE.md`, agent definition
files, Agent Skill files. Forbidden: config files (`*.json`, `*.yaml`, `*.toml`), source code.

**See**: [repo-governance/conventions/formatting/emoji.md](./repo-governance/conventions/formatting/emoji.md)

### Diagrams

Mermaid diagrams with color-blind friendly palette, proper accessibility.

**See**: [repo-governance/conventions/formatting/diagrams.md](./repo-governance/conventions/formatting/diagrams.md)

### Content Quality

Active voice, single H1, proper heading nesting, alt text for images, WCAG AA color contrast.

**See**: [repo-governance/conventions/writing/quality.md](./repo-governance/conventions/writing/quality.md)

### Dynamic Collection References

Never hardcode counts of dynamic collections (agents, skills, conventions, practices, principles,
workflows) in docs. Reference collection by name and link.

**See**: [repo-governance/conventions/writing/dynamic-collection-references.md](./repo-governance/conventions/writing/dynamic-collection-references.md)

## Development Practices

### Functional Programming

Prefer immutability, pure functions, functional core/imperative shell.

**See**: [repo-governance/development/pattern/functional-programming.md](./repo-governance/development/pattern/functional-programming.md)

### Implementation Workflow

Make it work → Make it right → Make it fast.

**See**: [repo-governance/development/workflow/implementation.md](./repo-governance/development/workflow/implementation.md)

### Test-Driven Development

Red → Green → Refactor. Required for all code changes. Every code delivery step uses the explicit
three-substep template (RED/GREEN/REFACTOR), each naming a file path, verbatim command, and acceptance
criterion.

**See**: [repo-governance/development/workflow/test-driven-development.md](./repo-governance/development/workflow/test-driven-development.md)

### Specs & Gherkin Completeness (Both Paths)

Code under `apps/`/`libs/` never lands without companion `specs/` Gherkin — **both** for direct changes
(same commit/PR; enforced by `specs:coverage` + `swe-code-checker`) and planned changes (plan carries
Gherkin steps; `plan-maker` emits them, `plan-checker` flags absence). Pure refactors and docs-only
changes are exempt.

**See**: [repo-governance/development/quality/feature-change-completeness.md](./repo-governance/development/quality/feature-change-completeness.md)

### Regression Test Mandate (Every Bug Fix)

Every bug fix lands with a reproducing test (failing before fix, passing after) in the same commit/PR —
blocking, no exemptions. Enforced by `swe-code-checker` (Step 6.7) and `plan-checker` (Step 16b).

**See**: [repo-governance/development/quality/regression-test-mandate.md](./repo-governance/development/quality/regression-test-mandate.md)

### Knowledge Capture

Every plan ends with a Knowledge Capture phase: `learnings.md` triaged to a home or discarded.

**See**: [knowledge-capture.md](./repo-governance/development/quality/knowledge-capture.md)

### Reproducible Environments

Volta for Node.js/npm pinning, package-lock.json, .env.example. **Hard iron rule — no secrets in
committed files**: Never commit system secrets to any git-tracked file — history is permanent. Real
values in uncommitted `.env*` (except `.env.example`). **Guardrail**: Agents must not
read/write/edit/commit real `.env*` files — only `.env.example` is permitted; scripts under
`apps/`/`libs/`/`scripts/` are exempt. **Git Identity Guardrail**: No AI agent sets or modifies
git identity at any scope — `git config --local user.*`, bare `git config user.*`,
`git config --global user.*`, `git config --system user.*`, or direct `.git/config [user]`
edits are all forbidden. Identity comes from the developer's global `~/.gitconfig` (optionally
`includeIf` for per-tree overrides). CI exemption: workflow YAML service-account identity
(e.g. `github-actions[bot]`) is not an agent action.

**See**: [repo-governance/development/workflow/reproducible-environments.md](./repo-governance/development/workflow/reproducible-environments.md),
[Secrets and Env Standards](./repo-governance/conventions/security/secrets-and-env-standards.md)

### Dependency Bump Stability & Safety Policy

Three-path tree: A (LTS latest patch), B (60-day soak + CVE-clean), C (security-override waiver).
Exact pins only, CVE-clean across NVD, GitHub Advisories, Snyk, vendor pages, CISA KEV. CISA-KEV
fast-track and EPSS ≥ 0.5 escalate to Path C.

**See**: [repo-governance/development/workflow/dependency-bump-policy.md](./repo-governance/development/workflow/dependency-bump-policy.md)

### Agent Workflow Orchestration

Plan mode for non-trivial tasks (3+ steps or architecture decisions). **Parallel-by-default**: run
independent sub-units in parallel under the **N+1 model** — `1 main thread + N background agents =
N+1 total`, **default N=3** (4 total). N=3 bounds token/compute-budget burn; raise it per-plan only
when independent work, machine capacity, and budget headroom all allow, lower it under pressure, and
never self-promote beyond the declared N. **Subagent concurrency**: poll mtime every 3 min; if stale
30 min, `TaskStop` and relaunch.
**Same-machine assumption**: always assume other agents, engineers, and processes run simultaneously
on the **same shared machine** — sharing its disk, git object store, worktrees, and CI runners — so
every orchestration and git action must be safe under concurrent actors.
**DAG-first**: every non-trivial task list and delivery checklist declares a dependency DAG
(`blocks`/`blockedBy`); independent nodes fan out up to N, dependent nodes serialize, cleanup is the
terminal node. DAG width is the fan-out — N only caps it.
**Background-slot preference**: fill background slots up to N, keeping the main thread vacant and
responsive (orchestrator, not worker) — never split dependent work to fill a slot.
**Status cadence**: update the user every **3-5 minutes, not faster**, while items are active.
**Task-list discipline**: maintain live task list for non-trivial work; mark in-progress before starting,
completed after verifying; add discovered tasks immediately.

**See**: [repo-governance/development/agents/agent-workflow-orchestration.md](./repo-governance/development/agents/agent-workflow-orchestration.md),
[Subagent Orchestration Convention](./repo-governance/development/agents/subagent-orchestration.md),
[Parallel-by-Default Practice](./repo-governance/development/practice/parallel-by-default.md),
[Task List Discipline](./repo-governance/development/practice/task-list-discipline.md),
[No Destructive Git Operations](./repo-governance/development/workflow/no-destructive-git-operations.md),
[Worktree and Artifact Cleanup](./repo-governance/development/workflow/worktree-and-artifact-cleanup.md)

### Manual Verification & CI Blockers

- **Verify behavior**: Playwright MCP for UI, curl for API.
  See [manual-behavioral-verification.md](./repo-governance/development/quality/manual-behavioral-verification.md)
- **User-facing delivery hardening**: Sixteen rules; near-end EWT/UWT/DWT retest for UI plans, AET
  for API plans. See [user-facing-delivery-hardening.md](./repo-governance/development/quality/user-facing-delivery-hardening.md)
- **CI blockers**: Investigate root cause, fix properly, never bypass.
  See [ci-blocker-resolution.md](./repo-governance/development/quality/ci-blocker-resolution.md)
- **CI post-push verification**: After pushing app or lib code, trigger CI and verify it passes.
  See [ci-post-push-verification.md](./repo-governance/development/workflow/ci-post-push-verification.md)
- **CI monitoring**: Poll every **2 minutes** — one `gh run view --json status,conclusion` per wakeup.
  Never tight-loop, never `gh run watch`. Rate-limited (403): wait ~35 min.
  See [ci-monitoring.md](./repo-governance/development/workflow/ci-monitoring.md)

## AI Agents

**Content Creation**: docs-{maker,tutorial-maker}, readme-maker, specs-maker,
apps-ayokoding-www-{general,by-example,annotated-concept,primer,in-the-field}-maker, apps-ose-www-content-maker, swe-ui-maker,
pr-review-maker

**Validation**: docs-{checker,tutorial-checker,link-checker,software-engineering-separation-checker},
readme-checker, specs-checker, apps-ayokoding-www-{general,by-example,annotated-concept,primer,in-the-field,facts,link}-checker,
apps-ose-www-content-checker, swe-{code,ui}-checker, ci-checker, web-researcher,
repo-{rules,workflow,harness-compatibility}-checker

**Fixing**: docs-{fixer,tutorial-fixer,software-engineering-separation-fixer,file-manager}, readme-fixer,
specs-fixer, apps-ayokoding-www-{general,by-example,annotated-concept,primer,in-the-field,facts,link}-fixer,
apps-ose-www-content-fixer, swe-ui-fixer, ci-fixer, repo-{rules,workflow,harness-compatibility}-fixer,
pr-review-fixer

**PR Review Cycle**: pr-review-{maker,fixer} — GitHub-Reviews-API-driven maker→fixer cycle for
`*-to-pr` Delivery Mode plans (see [Delivery Mode](./repo-governance/conventions/structure/plans.md#delivery-mode)
and [PR Review Quality Gate workflow](./repo-governance/workflows/pr/pr-review-quality-gate.md)).

**Testing**: web-{exploratory,usability,design}-tester (live-site triad: spec-aware / spec-blind /
design-aware); api-exploratory-tester (live REST/GraphQL, HTTP/curl-driven). All non-destructive; output
modes: `plan` (default), `delivery` (rule-15 retest), `local-temp`.

**Planning**: plan-{maker,checker,execution-checker,fixer}, repo-setup-manager. plan-maker grills user
before/after with multiple-choice options per
[Grilling-With-Options Convention](./repo-governance/development/workflow/grilling-with-options.md);
Phase 0 first, `[AI]`/`[HUMAN]` tags, gated phases. See
[plan-execution workflow](./repo-governance/workflows/plan/plan-execution.md) and
[plan-planning workflow](./repo-governance/workflows/plan/plan-planning.md).

**Development**: swe-{golang,typescript,e2e,csharp,fsharp,rust}-dev

**Operations**: apps-{ayokoding-www,ose-www,organiclever-www,organiclever-app-web,ose-app-web,wahidyankf-www,web-ui-storybook}-deployer

**Content**: pdf-to-md-{maker,checker,fixer}

**Meta**: agent-maker, repo-{rules,workflow}-maker, social-linkedin-post-maker

**Maker-Checker-Fixer Pattern**: Three-stage workflow with criticality levels (CRITICAL/HIGH/MEDIUM/LOW),
confidence assessment (HIGH/MEDIUM/FALSE_POSITIVE).

**Web Research Default**: `web-researcher` is the default primitive for public-web information gathering.
See [Web Research Delegation Convention](./repo-governance/conventions/writing/web-research-delegation.md).

**agent skills infrastructure**: Two modes — **Inline** (default: inject into current conversation) and
**Fork** (`context: fork`: delegated isolated context, return summarized results). Agent definition files
at `.claude/agents/<name>.md`; skill files at `.claude/skills/<name>/SKILL.md`. Agent skills serve agents
(service relationship, not governance).

**See**: [repo-governance/development/agents/ai-agents.md](./repo-governance/development/agents/ai-agents.md),
[repo-governance/development/pattern/maker-checker-fixer.md](./repo-governance/development/pattern/maker-checker-fixer.md),
[Agent Naming Convention](./repo-governance/conventions/structure/agent-naming.md),
[Workflow Naming Convention](./repo-governance/conventions/structure/workflow-naming.md)

## Repository Architecture

Six-layer governance hierarchy: Layer 0 (Vision — WHY we exist: democratize Shariah-compliant
enterprise), Layer 1 (Principles — WHY we value approaches), Layer 2 (Conventions — WHAT documentation
rules), Layer 3 (Development — HOW we develop), Layer 4 (AI Agents — WHO enforces rules), Layer 5
(Workflows — WHEN we compose agents/procedures). **agent skills**: delivery infrastructure (inline + fork
modes) serving agents — not a governance layer.

**See**: [repo-governance/repository-governance-architecture.md](./repo-governance/repository-governance-architecture.md)

## Web Sites

| App                  | Domain                                                   | Port | Prod Branch                 |
| -------------------- | -------------------------------------------------------- | ---- | --------------------------- |
| ose-www              | [oseplatform.com](https://oseplatform.com)               | 3100 | `prod-ose-www`              |
| ayokoding-www        | [ayokoding.com](https://ayokoding.com)                   | 3101 | `prod-ayokoding-www`        |
| organiclever-www     | [www.organiclever.com](https://www.organiclever.com/)    | 3200 | `prod-organiclever-www`     |
| organiclever-app-web | TBD                                                      | 3202 | `prod-organiclever-app-web` |
| wahidyankf-www       | [www.wahidyankf.com](https://www.wahidyankf.com/)        | 3201 | `prod-wahidyankf-www`       |
| ose-app-web          | [app.oseplatform.com](https://app.oseplatform.com) (TBD) | 3300 | `prod-ose-app-web` (TBD)    |
| ose-be               | api.oseplatform.com (F# / Giraffe / ASP.NET 10)          | 8302 | —                           |
| organiclever-be      | (F# / Giraffe / ASP.NET 10, Kubernetes)                  | 8202 | —                           |

Each app README at `apps/[app-name]/README.md` covers framework, deployment, E2E tests, and content
details. Staging branches: `stag-organiclever-app-web`, `stag-ose-app-web`.

## Temporary Files for AI Agents

- **`generated-reports/`**: Validation/audit reports. Pattern:
  `{agent-family}__{uuid-chain}__{YYYY-MM-DD--HH-MM}__audit.md`. Checkers MUST write progressive reports.
- **`local-temp/`**: Misc temporary files.

**See**: [repo-governance/development/infra/temporary-files.md](./repo-governance/development/infra/temporary-files.md)

## Plans

`plans/` folder: `ideas.md` (1-3 liner ideas), `backlog/` (future; `YYYY-MM-DD__[id]/`),
`in-progress/` (active; `[id]/`), `done/` (completed; `YYYY-MM-DD__[id]/`).

**See**: [repo-governance/conventions/structure/plans.md](./repo-governance/conventions/structure/plans.md)

## Important Notes

- **Never commit secrets** (hard iron rule): No system secret goes into any git-tracked file; real values
  belong in uncommitted `.env*` (except `.env.example`). See [Secrets and Env Standards](./repo-governance/conventions/security/secrets-and-env-standards.md).
- **Do NOT stage or commit** unless explicitly instructed. Per-request commits one-time only.
- **License**: MIT. See [LICENSING-NOTICE.md](./LICENSING-NOTICE.md)
- **Agent invocation**: Use natural language to invoke agents/workflows
- **Token budget**: Don't worry about token limits — reliable compaction available
- **No time estimates**: Never give time estimates. Focus on what needs doing, not how long.

## Related Documentation

- **Conventions Index**: [repo-governance/conventions/README.md](./repo-governance/conventions/README.md) — Documentation writing and org standards
- **Development Index**: [repo-governance/development/README.md](./repo-governance/development/README.md) — Software dev practices and workflows
- **Principles Index**: [repo-governance/principles/README.md](./repo-governance/principles/README.md) — Foundational values governing all layers
- **Primary Binding Agents Index**: [agent catalog](./.claude/agents/README.md) — Specialized agents organized by role
- **Workflows Index**: [repo-governance/workflows/README.md](./repo-governance/workflows/README.md) — Orchestrated processes
- **Repository Architecture**: [repo-governance/repository-governance-architecture.md](./repo-governance/repository-governance-architecture.md) — Six-layer governance hierarchy

## Related Repositories

Three independent sibling repositories (no parent coordination repo):

- [`ose-public`](https://github.com/wahidyankf/ose-public) — this repo; upstream source of truth for
  scaffolding. MIT licensed.
- [`ose-primer`](https://github.com/wahidyankf/ose-primer) — downstream public template (scaffolding
  layer: governance, AI agents, skills, conventions, CI harness, polyglot demo apps). MIT licensed.
- [`ose-infra`](https://github.com/wahidyankf/ose-infra) — private infrastructure repo (GitHub Actions
  runner stack, `coralpolyp` app). Proprietary; not publicly accessible.

Content parity between `ose-public` and `ose-primer` maintained via
[plan-multi-repo-parity-planning](./repo-governance/workflows/plan/plan-multi-repo-parity-planning.md)
workflow. `ose-infra` does not participate in the parity loop.

`apps/rhino-cli` must be byte-identical (zero carve-outs) across all three repos, including its
Gherkin behavior tree at `specs/apps/rhino/behavior/rhino-cli/gherkin/**`, per the
[SDLC Gate Standard](./docs/reference/sdlc-gate-standard.md#rhino-cli-byte-identity-boundary).

See: [Related Repositories reference](./docs/reference/related-repositories.md).

## Models

Model selection by capability tier: **Planning-grade** (complex multi-step planning),
**Execution-grade** (standard coding and review), **Fast** (simple/low-latency). Concrete vendor model
IDs in each platform binding's agent definition files.

See [repo-governance/development/agents/model-selection.md](./repo-governance/development/agents/model-selection.md).

## General Guidelines for Working with Nx

- For navigating/exploring the workspace, invoke the `nx-workspace` skill first — it has patterns for
  querying projects, targets, and dependencies
- When running tasks (build, lint, test, e2e, etc.), prefer running through `nx` (`nx run`,
  `nx run-many`, `nx affected`) instead of underlying tooling directly
- Prefix nx commands with the workspace package manager (e.g., `pnpm nx build`, `npm exec nx test`)
- You have access to the Nx MCP server and its tools; use them
- For Nx plugin best practices, check `node_modules/@nx/<plugin>/PLUGIN.md`. Not all plugins have this
  file — proceed without it if unavailable.
- NEVER guess CLI flags — check nx_docs or `--help` first when unsure

## Scaffolding & Generators

For scaffolding tasks (creating apps, libs, project structure, setup), ALWAYS invoke the `nx-generate`
skill FIRST before exploring or calling MCP tools.

## When to use nx_docs

- USE for: advanced config options, unfamiliar flags, migration guides, plugin config, edge cases
- DON'T USE for: basic generator syntax (`nx g @nx/react:app`), standard commands, things you already
  know
- The `nx-generate` skill handles generator discovery internally — don't call nx_docs just to look up
  generator syntax

## Platform Binding Examples

The content under this heading is intentionally vendor-specific. Per the
[Governance Vendor-Independence Convention](./repo-governance/conventions/structure/governance-vendor-independence.md),
the vendor-audit scanner skips every line under a "Platform Binding Examples"
heading until the next same-level heading or end of file.

### Platform Bindings Catalog

Concrete tool integrations live **outside** `repo-governance/` in platform-binding directories:

- **Claude Code** → `.claude/`, with `CLAUDE.md` as the Claude-Code-discoverable shim importing this file
- **OpenCode** → `.opencode/agents/` (auto-synced from `.claude/`); reads this file (`AGENTS.md`)
  natively; reads agent skill files at `.claude/skills/<name>/SKILL.md` natively
- **OpenAI Codex CLI** → reads `AGENTS.md` natively (`.codex/config.toml` present)
- **GitHub Copilot, Cursor, Windsurf, JetBrains Junie, Google Antigravity CLI, Pi** → read root
  `AGENTS.md` natively (Tier-1); no per-tool instruction file shipped by default (see no-shadowing rule)
- **Amazon Q Developer** (sunsetting — IDE plugins EOS 2027-04-30; succeeded by **Kiro CLI**, which
  reads `AGENTS.md` natively) → does not read `AGENTS.md` natively; receives a generated bridge under
  `.amazonq/` (`rules/00-agents-md.md` + a default agent config), emitted by `rhino-cli agents emit-bindings`
- **Aider** → reads `CONVENTIONS.md` natively per Aider's own docs
  (<https://aider.chat/docs/usage/conventions.html>); the agents.md standard site lists Aider as a
  supported tool but Aider's own documentation does not document AGENTS.md specifically
- **Future**: `CONVENTIONS.md` (Aider)

See [docs/reference/platform-bindings.md](./docs/reference/platform-bindings.md) for the full catalog
of binding directories, root instruction files, and mechanical translation artifacts. The two-tier
binding model and no-shadowing rule are defined in
[repo-governance/conventions/structure/multi-harness-binding.md](./repo-governance/conventions/structure/multi-harness-binding.md).

### Concrete Vendor Model IDs

Concrete vendor model IDs live in each platform binding's agent definition files (e.g.,
`.claude/agents/<name>.md` frontmatter for the primary platform binding).
