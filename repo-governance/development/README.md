---
description: Internal development guidance for authorized open-sharia-enterprise delivery work
when_to_use: Use when you are authorized to plan, build, verify, or land repository work and need the practice governing a specific step.
---

# Development

This is the internal guide to delivering changes safely and consistently in
open-sharia-enterprise. Use it when you are already authorized to plan, build, verify, or land
repository work.

## Scope

This directory answers one practical question: **how do authorized teams develop software in
this repository?** It covers software delivery practices, tools, controls, and workflows. It
does not duplicate documentation-writing rules — for those, see [Conventions](../conventions/README.md).

**Governance**: All development practices serve the [Vision](../vision/open-sharia-enterprise.md)
(Layer 0), implement the [Core Principles](../principles/README.md) (Layer 1), and
implement/enforce [Documentation Conventions](../conventions/README.md) (Layer 2). See
[Repository Governance Architecture](../repository-governance-architecture.md) for the full model.

## Subdirectory Index

- [Behaviour-Driven Development](./behaviour-driven-development.md) — Canonical Gherkin corpus,
  Unit/Integration/E2E boundaries, applicable adapters, exemptions, static coverage, and semantic
  review. Use before changing observable behaviour or test topology.
- [Workflow Development](./workflow/README.md) — Development workflow conventions governing how contributors and agents execute work — TDD, commits, branching, environment reproducibility, grilling, and CI. Use when looking for the standard covering a step of development work — implementation, git, commits, environment setup, CI, or grilling a design decision.
- [Quality Development](./quality/README.md) — Quality standards and evidence practices for trustworthy repository changes. Use to decide what evidence, test, or validation a change needs before it can be trusted.
- [Development Patterns](./pattern/README.md) — Reusable architecture and quality patterns for maintainable platform changes. Use when a change needs a proven shape — an application boundary, an audit trail, or an independent review cycle.
- [Development Practices](./practice/README.md) — Day-to-day practices for solving repository work carefully and collaboratively. Use when the work is ambiguous, shared, or already in motion, and you need a behavioural practice rather than a code pattern or tool configuration.
- [AI Agents Development](./agents/README.md) — Standards for AI agents that work safely and predictably in this repository. Use when defining or changing an AI agent, or when deciding where an agent-development topic belongs.
- [Infrastructure Development](./infra/README.md) — Standards for reliable local development infrastructure, toolchains, and artifacts. Use when setting up local development tooling, naming Nx targets, organizing temporary files, or writing testable acceptance criteria.
- [Frontend Development](./frontend/README.md) — UI development conventions for the open-sharia-enterprise monorepo's frontend applications. Use when building, styling, or testing a UI component in any frontend app in this monorepo.

## Related Documentation

- [Repository Governance Architecture](../repository-governance-architecture.md) — Complete six-layer architecture (Layer 3: Development).
- [Core Principles](../principles/README.md) — Layer 1: Foundational values that govern development practices.
- [Conventions](../conventions/README.md) — Layer 2: Documentation conventions (parallel governance with development).
- [Workflows](../workflows/README.md) — Layer 5: Multi-step processes composing agents, procedures, and/or other workflows.
