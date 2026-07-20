---
title: "Workflows"
description: Orchestrated multi-step processes that compose agents, procedures, and/or other workflows to achieve specific goals
category: explanation
subcategory: workflows
tags:
  - index
  - workflows
  - orchestration
  - agents
created: 2026-01-04
---

# Workflows Index

**Purpose**: Orchestrated multi-step processes that compose agents, procedures, and/or other workflows to achieve specific goals with clear termination criteria.

**Layer**: 5th layer in repository hierarchy (composes agents, procedures, and/or other workflows)

## What Are Workflows?

Workflows are **composed processes** that:

- 🔄 Orchestrate sequences of agents, procedures, and/or other workflows — in any combination
- 🎯 Have clear goals and termination criteria
- 📊 Manage state between steps
- ⚡ Support parallel, sequential, and conditional execution
- 👤 Include human approval checkpoints
- ♻️ Are reusable and composable — workflows can nest other workflows
- 🔁 Can loop until termination criteria are met

**Key insight**: Workflows are to Agents what Agents are to Tools - a composition layer. A workflow step can itself be another workflow.

## Repository Hierarchy

Workflows are **Layer 5** in the six-layer architecture. See [Repository Governance Architecture](../repository-governance-architecture.md) for complete governance model.

```
Layer 0: Vision (WHY WE EXIST)     → Foundational purpose
Layer 1: Principles (WHY)          → Foundational values
Layer 2: Conventions (WHAT)        → Documentation rules
Layer 3: Development (HOW)         → Software practices
Layer 4: AI Agents (WHO)           → Atomic task executors
Layer 5: Workflows (WHEN)          → Multi-step processes ← YOU ARE HERE
```

## Quick Start

### Understanding Workflows

1. Read [Workflow Pattern Convention](meta/README.md) for structure and rules
2. Create workflows as needed following the convention patterns
3. Review workflow families below

### Using Workflows

**How to execute workflows**:

```
User: "Run [workflow-name] workflow for [scope] in [mode] mode"
```

Workflows support two execution modes (see [Workflow Execution Mode Convention](meta/README.md)):

**Agent Delegation (preferred)**: Invoke specialized agents via the Agent tool with `subagent_type`. Each agent runs in an isolated context, returns results to the orchestrating conversation, and file changes persist to the filesystem.

**Manual Orchestration (fallback)**: When agents are unavailable as delegated agent types, the AI assistant follows workflow steps directly using Read/Write/Edit tools in the main execution context.

All workflows support standard input parameters:

- **mode**: Quality threshold (lax/normal/strict/ocd) - default: strict (for workflows that have a `mode` parameter)
- **max-concurrency**: Background agents run concurrently — the N in the N+1 model (`1 main thread + N background agents = N+1 total`) - default: 3
- **min-iterations**: Minimum check-fix cycles - optional
- **max-iterations**: Maximum check-fix cycles - optional

## Workflow Directories

- [ayokoding-web/README.md](ayokoding-web/README.md) — AyoKoding web content quality workflows
- [ci/README.md](ci/README.md) — CI/CD standards compliance workflows
- [docs/README.md](docs/README.md) — Documentation quality workflows
- [infra/README.md](infra/README.md) — Infrastructure and environment setup workflows
- [meta/README.md](meta/README.md) — Workflow system reference documentation
- [content/README.md](content/README.md) — Content conversion and fidelity validation workflows (PDF-to-Markdown)
- [api/README.md](api/README.md) — Live REST/GraphQL API quality workflows
- [pr/pr-review-quality-gate.md](pr/pr-review-quality-gate.md) — PR review maker→fixer cycle workflow (single-file directory, no category `README.md` yet)
- [plan/README.md](plan/README.md) — Project planning workflows
- [repo/README.md](repo/README.md) — Repository governance workflows
- [specs/README.md](specs/README.md) — Specification quality workflows
- [ui/README.md](ui/README.md) — UI component quality workflows
- [web/README.md](web/README.md) — Live-website testing and fix-planning workflows

## Available Workflows

| Workflow                                                                     | Purpose                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Agents Used                                                                                                                                                             | Complexity |
| ---------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| [Repository Rules Validation](repo/README.md)                                | Run deterministic preflight (CLI orchestrator) then validate residual AI-only categories iteratively until ZERO findings                                                                                                                                                                                                                                                                                                                                                                                          | repo-rules-checker, repo-rules-fixer                                                                                                                                    | Medium     |
| [Repository Harness Compatibility Quality Gate](repo/README.md)              | Phase 0: validate five deterministic cross-vendor parity invariants; Phase 1: detect external drift between supported harness conventions and the platform-binding catalog; fix both iteratively to double-zero                                                                                                                                                                                                                                                                                                   | repo-harness-compatibility-checker, repo-harness-compatibility-fixer                                                                                                    | Medium     |
| [Dependency Bump Planning](repo/README.md)                                   | Survey every dependency manifest across `apps/` and `libs/`, classify each candidate bump per the Dependency Bump Stability & Safety Policy (three-path tree + Rule 5a/5b), and produce a validated **backlog** plan that will perform the bumps. Deliverable is the plan, not the edits.                                                                                                                                                                                                                         | web-researcher, plan-maker, plan-checker, plan-fixer                                                                                                                    | Medium     |
| [Plan Multi-Repo Parity Planning](plan/README.md)                            | Survey multiple sibling repos, build a cross-repo deviation matrix, grill every gap to a recorded decision (first grill, hard gate), verify external claims via web research, re-grill on the findings, then author one aligned-but-deliberately-divergent plan per repo and gate each to double-zero                                                                                                                                                                                                             | plan-maker, web-researcher, plan-checker, plan-fixer                                                                                                                    | High       |
| [Plan Multi-Repo Parity Planning and Execution](plan/README.md)              | End-to-end composite: full parity planning (survey, matrix, two grills, research, author, gate, deliver), then a third pre-execution grill, then plan-execution per repo to zero findings — flattened granular Task list synced 1:1 with each delivery.md, archival, and prompted worktree cleanup                                                                                                                                                                                                                | plan-maker, web-researcher, plan-checker, plan-fixer, plan-execution-checker, repo-setup-manager                                                                        | High       |
| [Plan Quality Gate](plan/README.md)                                          | Validate plan completeness and accuracy, apply fixes iteratively until ZERO findings                                                                                                                                                                                                                                                                                                                                                                                                                              | plan-checker, plan-fixer                                                                                                                                                | Medium     |
| [Plan Execution](plan/README.md)                                             | Execute plan tasks systematically with validation and completion tracking (calling context orchestrates, delegates per-item to specialized agents)                                                                                                                                                                                                                                                                                                                                                                | plan-execution-checker                                                                                                                                                  | Medium     |
| [Multi-Plans Execution](plan/README.md)                                      | Execute several plans together — an explicit list or a set-selector (`all-in-progress` / `all-backlog` / `all`, optionally minus an `except` list) resolved to a frozen set: build a dependency DAG (explicit `Depends-on` wins, resource-overlap inference fills gaps), materialize one very-granular union Task list, and run a bounded ready-queue scheduler (default 3 parallel nodes, overridable) driving each plan through its full plan-execution lifecycle; failure quarantines a plan without cascading | plan-execution-checker, plan-checker, plan-fixer, pr-review-maker, pr-review-fixer                                                                                      | High       |
| [Documentation Quality Gate](docs/README.md)                                 | Validate all docs/ content quality (factual accuracy, pedagogical structure, link validity), apply fixes iteratively until ZERO findings                                                                                                                                                                                                                                                                                                                                                                          | docs-checker, docs-tutorial-checker, docs-link-checker, docs-fixer, docs-tutorial-fixer                                                                                 | High       |
| [AyoKoding Web General Quality Gate](ayokoding-web/README.md)                | Validate all ayokoding-web content quality (factual accuracy, links), apply fixes iteratively until ZERO findings                                                                                                                                                                                                                                                                                                                                                                                                 | apps-ayokoding-www-general-checker, apps-ayokoding-www-facts-checker, apps-ayokoding-www-link-checker, apps-ayokoding-www-general-fixer, apps-ayokoding-www-facts-fixer | High       |
| [AyoKoding Web By-Example Quality Gate](ayokoding-web/README.md)             | Validate by-example tutorial quality (95% coverage through 75-85 examples) and apply fixes iteratively until EXCELLENT status achieved                                                                                                                                                                                                                                                                                                                                                                            | apps-ayokoding-www-by-example-checker, apps-ayokoding-www-by-example-fixer                                                                                              | Medium     |
| [AyoKoding Web Annotated-Concept Quality Gate](ayokoding-web/README.md)      | Validate Annotated-concept tutorial quality (45-60 worked examples, or 20-30 scenarios for the leadership no-code sub-mode) and apply fixes iteratively until EXCELLENT status achieved                                                                                                                                                                                                                                                                                                                           | apps-ayokoding-www-annotated-concept-checker, apps-ayokoding-www-annotated-concept-fixer                                                                                | Medium     |
| [AyoKoding Web Primer Quality Gate](ayokoding-web/README.md)                 | Validate Primer ("Just Enough X") tutorial quality (75-85 examples authored at By-Example pace, scope discipline) and apply fixes iteratively until EXCELLENT status achieved                                                                                                                                                                                                                                                                                                                                     | apps-ayokoding-www-primer-checker, apps-ayokoding-www-primer-fixer                                                                                                      | Medium     |
| [AyoKoding Web In-the-Field Quality Gate](ayokoding-web/README.md)           | Validate in-the-field production guide quality and apply fixes iteratively until EXCELLENT status achieved                                                                                                                                                                                                                                                                                                                                                                                                        | apps-ayokoding-www-in-the-field-checker, apps-ayokoding-www-in-the-field-fixer                                                                                          | Medium     |
| [Documentation Software Engineering Separation Quality Gate](docs/README.md) | Validate software engineering documentation separation between OSE Platform style guides and AyoKoding educational content, apply fixes iteratively until ZERO findings                                                                                                                                                                                                                                                                                                                                           | docs-software-engineering-separation-checker, docs-software-engineering-separation-fixer                                                                                | Medium     |
| [Specs Validation](specs/README.md)                                          | Validate specs/ directory for structural completeness, content accuracy, cross-spec consistency, and C4 diagram correctness, apply fixes iteratively until ZERO findings                                                                                                                                                                                                                                                                                                                                          | specs-checker, specs-fixer                                                                                                                                              | Medium     |
| [UI Quality Gate](ui/README.md)                                              | Validate UI component quality (tokens, accessibility, patterns, dark mode, responsive), apply fixes iteratively until ZERO findings                                                                                                                                                                                                                                                                                                                                                                               | swe-ui-checker, swe-ui-fixer                                                                                                                                            | Medium     |
| [API Quality Gate](api/README.md)                                            | Exercise a live REST/GraphQL API against its contract and specs, fix findings, re-test until the defect set is empty                                                                                                                                                                                                                                                                                                                                                                                              | api-exploratory-tester, `swe-*-dev`                                                                                                                                     | Medium     |
| [CI Quality Gate](ci/README.md)                                              | Validate all projects conform to CI/CD standards (Nx targets, coverage, Docker, Gherkin, workflows), apply fixes iteratively until ZERO findings                                                                                                                                                                                                                                                                                                                                                                  | ci-checker, ci-fixer                                                                                                                                                    | Medium     |
| [PDF-to-Markdown Quality Gate](content/README.md)                            | Convert PDF to verbatim Markdown and validate conversion fidelity (text completeness, tables, figures, Mermaid, OCR) iteratively until ZERO findings on two consecutive checks                                                                                                                                                                                                                                                                                                                                    | pdf-to-md-maker, pdf-to-md-checker, pdf-to-md-fixer                                                                                                                     | Medium     |
| [Development Environment Setup](infra/README.md)                             | Install and verify all 18+ polyglot toolchains required for development, testing, and git hooks across all projects                                                                                                                                                                                                                                                                                                                                                                                               | (manual orchestration — developer-guided)                                                                                                                               | High       |
| [Web UX Test-Fixing Planning](web/README.md)                                 | Run the three live-site testers — `web-exploratory-tester` (spec-aware correctness), `web-usability-tester` (spec-blind usability), and `web-design-tester` (design-aware fidelity) — against the same live URL(s) and goal, then synthesize all three result sets into one fix-ready plan — findings stay source-attributed (EWT-### vs UWT-### vs DWT-###), plus `tech-docs.md` and a TDD-shaped `delivery.md`. Deliverable is the plan, not the fixes.                                                         | web-exploratory-tester, web-usability-tester, web-design-tester, plan-maker, plan-checker, plan-fixer                                                                   | High       |
| [PR-Review Maker→Fixer Cycle](pr/pr-review-quality-gate.md)                  | Run a strictly sequential N-cycle (default 3) `pr-review-maker` → `pr-review-fixer` loop against a pull request — post line-anchored findings via the GitHub Reviews API, triage and resolve every thread, gate on CI-green between cycles — until the `*-to-pr` done-definition (N cycles complete, every comment answered, gates green, archival-in-PR committed) is satisfied. Mandatory pre-merge gate for the `worktree-to-pr` and `main-to-pr` delivery modes, invoked from Plan Execution Step 8.          | pr-review-maker, pr-review-fixer                                                                                                                                        | Medium     |

All _-quality-gate workflows follow the [_-check-fix Workflow Pattern](meta/README.md) which fixes ALL findings (CRITICAL, HIGH, MEDIUM, LOW criticality levels) and iterates until ZERO findings remain.

## Naming Rule

Every workflow filename follows: `<scope>(-<qualifier>)*-<type>`

- `scope` — top-level domain matching the parent directory (`ci`, `docs`, `plan`, `pr`, `repo`, `specs`, `ui`, `web`, `infra`, `ayokoding-web`, etc.).
- `qualifier` — zero or more refinement tokens (e.g., `rules`, `by-example`, `software-engineering-separation`).
- `type` — exactly one trailing token from the Type Vocabulary below.

No other structure is permitted. No exceptions, except for reference material under `repo-governance/workflows/meta/` (documented below).

Normative source: [Workflow Naming Convention](../conventions/structure/workflow-naming.md).

## Type Vocabulary

| Type           | Semantics                                                                                                | Example workflows                                            |
| -------------- | -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| `quality-gate` | Iterative maker → checker → fixer loop until zero findings                                               | `ci-quality-gate`, `plan-quality-gate`, `specs-quality-gate` |
| `execution`    | Executes a defined procedure or plan against inputs                                                      | `plan-execution`                                             |
| `setup`        | One-time environment or resource provisioning                                                            | `development-environment-setup`                              |
| `planning`     | Surveys/analyzes state and produces a plan in `plans/` as its terminal deliverable (never implements it) | `repo-dependency-bump-planning`                              |

## Meta reference exception

Files under `repo-governance/workflows/meta/` are **reference documentation about the workflow system** (e.g., `execution-modes.md`, `workflow-identifier.md`). They describe how workflows work, not workflows themselves. They are exempt from the type-suffix rule.

Enforcement: `rhino-cli repo-governance workflows naming validate` (wired into pre-push and CI).

## Workflow Families

### Documentation Workflows

Workflows for creating and validating documentation:

- **docs**: Project documentation (tutorials, how-to, reference, explanation)
- **readme**: README.md quality and engagement (planned - no workflow file yet)
- **plan**: Project planning documents — establishment, multi-repo parity planning (with and without composite execution), quality gate, and execution

### Web Content Workflows

Workflows for web application content (Next.js sites):

- **ayokoding-web**: ayokoding-web content creation and validation
- **ayokoding-facts**: Factual accuracy validation for ayokoding-web (planned - no workflow file yet)
- **ayokoding-structure**: Navigation structure and weight management (planned - no workflow file yet)
- **ose-web-content**: ose-web content (planned - no workflow file yet)

### Specification Workflows

Workflows for specification quality:

- **specs**: Validate specs/ for structural completeness, content accuracy, cross-spec consistency, C4 diagrams

### UI Workflows

Workflows for UI component quality:

- **ui**: UI component quality validation (tokens, accessibility, patterns, dark mode, responsive)

### API Workflows

Workflows for live REST/GraphQL API quality:

- **api-quality-gate**: Exercise a running API against its contract (OpenAPI 3.x / GraphQL SDL) and
  existing Gherkin, fix findings, re-test until none remain. Tester-driven
  (`api-exploratory-tester` → `swe-*-dev`), not a checker/fixer pair

### CI/CD Workflows

Workflows for CI/CD standards compliance:

- **ci-quality-gate**: Validate all projects conform to CI/CD conventions (Nx targets, coverage, Docker, Gherkin, workflows)

### Content Workflows

Workflows for content conversion and fidelity validation:

- **pdf-to-md-quality-gate**: Convert PDF → Markdown (text-based or OCR), validate completeness
  and accuracy iteratively until ZERO findings on two consecutive checks

### Infrastructure Workflows

Workflows for development environment and infrastructure:

- **development-environment-setup**: Install and verify all toolchains for local development

### Web Testing Workflows

Workflows that test a live running website and turn findings into a fix plan:

- **web-ux-test-fixing-planning**: Run the three live-site testers — spec-aware exploratory (correctness), spec-blind heuristic-usability, and design-aware design-fidelity — against the same live URL(s) and goal sequentially (integrating each before the next), then solidify one fix-ready plan (source-attributed findings EWT-###/UWT-###/DWT-### + `tech-docs.md` + TDD `delivery.md` + an `assets/` UI-mockup folder when UI-bearing) in `plans/in-progress/`, grilling the user on every material decision. This is the near-end three-tester round web-UI feature-change plans must run (User-Facing Delivery Hardening Rule 15)

### PR Review Workflows

Workflows for reviewing and finishing off pull requests before the merge:

- **pr-review-quality-gate**: Strictly sequential N-cycle (default 3) `pr-review-maker` →
  `pr-review-fixer` loop against a PR — line-anchored findings via the GitHub Reviews API, per-thread
  triage and resolution, CI-green gate between cycles — mandatory before archival and the
  merge for the `worktree-to-pr` and `main-to-pr` delivery modes

### Repository Governance Workflows

Workflows for repository rules and cross-vendor consistency:

- **repo-rules**: Validate consistency across principles, conventions, development, agents, AGENTS.md
- **repo-parity**: Validate cross-vendor behavioral-parity invariants (vendor-neutrality, sync no-op, count parity, color/tier-map coverage)
- **repo-harness-compatibility**: Validate cross-harness compatibility between platform-binding catalog and upstream coding-agent harness conventions
- **ose-primer**: Sync content between `ose-public` and the downstream `ose-primer` template (adopt, propagate, parity-check)
- **repo-dependency-bump-planning**: Survey all `apps/` + `libs/` dependency manifests, classify per the Dependency Bump Stability & Safety Policy, and produce a validated backlog plan that will perform the bumps

## Step Execution Patterns

Workflows support three step execution patterns:

### Sequential

Steps execute one after another:

```
Step 1 → Step 2 → Step 3 → Step 4
```

Later steps can reference outputs from earlier steps.

**Use when:** Step N requires outputs from step N-1 (e.g., Maker-Checker-Fixer where fixer needs checker's audit report).

### Parallel

Steps execute simultaneously:

```
        ┌─ Step 2a ─┐
Step 1 ─┼─ Step 2b ─┼─ Step 3
        └─ Step 2c ─┘
```

Improves efficiency when steps are independent.

**Use when:** Steps are independent and can run simultaneously for speed (e.g., validating multiple content types in parallel).

### Conditional

Steps execute only if conditions are met:

```
Step 1 → Step 2 (checkpoint) → Step 3 (if approved)
                            └→ Skip to Step 5 (if rejected)
```

Enables branching logic and human decision points.

**Use when:** Workflow branches based on user decisions or validation results (e.g., deploy to production only if tests pass).

## Human Checkpoints

Workflows pause for user approval at critical points:

- 🔍 **Review audit reports** - Before applying fixes
- ✅ **Approve deployments** - Before pushing to production
- 🎯 **Choose approach** - When multiple valid options exist
- 🛑 **Handle errors** - When automated recovery is insufficient

Human checkpoints use the `AskUserQuestion` tool.

## State Management

Workflows pass data between steps using references:

- `{input.name}` - Workflow input parameters
- `{stepN.outputs.name}` - Output from step N
- `{stepN.status}` - Status of step N (success/fail/partial)
- `{stepN.user-approved}` - User decision from checkpoint

## Workflow vs Plans

| Aspect    | Plans                              | Workflows                                    |
| --------- | ---------------------------------- | -------------------------------------------- |
| Purpose   | Strategic planning (WHAT to build) | Tactical execution (HOW to build)            |
| Audience  | Humans                             | Agents + Humans                              |
| Format    | Free-form Markdown                 | Structured Markdown with YAML                |
| Execution | Manual, guided by human            | Automated, orchestrated by workflow executor |
| Lifecycle | Created → Updated → Archived       | Created → Executed repeatedly → Deprecated   |
| Location  | `plans/` directory                 | `repo-governance/workflows/`                 |

**Relationship**: Plans can reference workflows ("Use deployment-workflow for release"). Workflows can be generated from plan checklists.

## Creating New Workflows

To create a new workflow:

1. **Identify need**: 2 or more agents, procedures, or workflows needed in sequence, or repeated process, or complex orchestration
2. **Design structure**: Define inputs, steps, outputs, goals, termination criteria
3. **Write workflow file**: Use plain descriptive name in the appropriate subdirectory of `repo-governance/workflows/[category]/`
4. **Document thoroughly**: Purpose, when to use, example usage, related workflows
5. **Validate**: Check frontmatter schema, agent references, dependencies
6. **Test manually**: Run workflow steps to verify correctness
7. **Add to index**: Update this README with workflow description

See [Workflow Pattern Convention](meta/README.md) for complete requirements.

## Validation

All workflows should be validated for:

- ✅ **Frontmatter completeness** - All required fields present
- ✅ **Agent existence** - All referenced agents exist in the primary binding directory (`.claude/agents/`) or secondary directories (`.opencode/agents/`)
- ✅ **Type correctness** - Inputs/outputs use valid types
- ✅ **Dependency acyclicity** - No circular step dependencies
- ✅ **Reference resolution** - All `{stepN.outputs}` references resolve
- ✅ **File naming** - Plain name in correct subdirectory of `repo-governance/workflows/`
- ✅ **Documentation quality** - Clear purpose, examples, termination criteria

Future: `workflow-validator` agent will automate this validation.

## Metrics and Observability

Track workflow performance:

- **Execution count** - How often workflows run
- **Success rate** - Percentage reaching "success" termination
- **Failure modes** - Common reasons for "partial" or "fail"
- **Step duration** - Time spent in each step (if measured)
- **Human intervention** - How often checkpoints pause workflows

## Principles Implemented/Respected

All workflows must respect core principles:

- ✅ **Explicit Over Implicit** - All steps, dependencies, conditions visible
- ✅ **Automation Over Manual** - Automate complex multi-step processes
- ✅ **Simplicity Over Complexity** - Break complex workflows into smaller ones
- ✅ **Progressive Disclosure** - Simple workflows stay simple
- ✅ **Accessibility First** - Human-readable format, clear documentation
- ✅ **No Time Estimates** - Define WHAT and HOW, not WHEN or HOW LONG

## Related Documentation

### Core Documentation

- [Workflow Pattern Convention](meta/README.md) - How workflows are structured
- [Maker-Checker-Fixer Pattern](../development/pattern/maker-checker-fixer.md) - Core workflow pattern
- [AI Agents Convention](../development/agents/ai-agents.md) - How agents work

### Supporting Documentation

- [Fixer Confidence Levels](../development/quality/fixer-confidence-levels.md) - How fixers assess changes
- [Content Preservation](../development/quality/content-preservation.md) - Preserving meaning during fixes
- [Temporary Files](../development/infra/temporary-files.md) - Where workflow outputs go
- [Plans Organization](../conventions/structure/plans.md) - How plans relate to workflows

### Layer Documentation

- [Repository Governance Architecture](../repository-governance-architecture.md) - Complete six-layer architecture explanation
- [Vision](../vision/open-sharia-enterprise.md) - Layer 0: Foundational purpose
- [Core Principles](../principles/README.md) - Layer 1: Foundational values
- [Conventions](../conventions/README.md) - Layer 2: Documentation rules
- [Development](../development/README.md) - Layer 3: Software practices
- [AI Agents](../../.claude/agents/README.md) - Layer 4: Task executors

## Future Enhancements

Planned workflow features:

- 🤖 **Workflow Executor Agent** - Automate workflow execution
- 📊 **Workflow Visualization** - Auto-generate diagrams from definitions
- 🧪 **Workflow Testing** - Dry-run mode, validation suite
- 📈 **Metrics Dashboard** - Track workflow performance
- ⏱️ **Timeouts and Retries** - Handle long-running or failing steps
- 🔙 **Rollback Support** - Undo steps on failure

## Questions?

- **What is a workflow?** - A composed multi-step process orchestrating agents, procedures, and/or other workflows
- **When should I create a workflow?** - When 2 or more agents, procedures, or workflows are used repeatedly in sequence or in composition
- **How do I run a workflow?** - Use manual orchestration (see "Using Workflows" above)
- **Can workflows call other workflows?** - Yes, workflows are composable
- **Do workflows replace agents?** - No, workflows orchestrate agents
- **Do workflows replace plans?** - No, plans are strategic, workflows are tactical

See [Workflow Pattern Convention](meta/README.md) and [Execution Modes Convention](meta/README.md) for comprehensive answers.
