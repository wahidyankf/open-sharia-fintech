---
name: development-environment-setup
title: "development-environment-setup"
description: "Guides installing and verifying every toolchain needed for pre-commit, pre-push, integration, and E2E work in this monorepo."
when_to_use: "Use for new developer onboarding, a fresh machine/OS setup, or recovering a broken toolchain."
goal: "Set up a complete local development environment with all toolchains required for pre-commit, pre-push, integration tests, and E2E tests across all projects"
termination: "npm run doctor reports all tools OK and nx affected -t test:quick passes for all projects"
inputs:
  - name: platform
    type: enum
    values: [macos, linux]
    description: Target operating system
    required: false
    default: macos
  - name: scope
    type: enum
    values: [full, minimal]
    description: "full: all 19 tools for all projects; minimal: core tools only (Node.js, Go, Docker, jq)"
    required: false
    default: full
outputs:
  - name: doctor-status
    type: enum
    values: [all-ok, warnings, missing]
    description: Result of npm run doctor after setup
  - name: tools-installed
    type: number
    description: Count of tools successfully installed and verified
---

# Development Environment Setup Workflow

**Purpose**: Guide a developer (or AI assistant helping a developer) through installing and
configuring every tool required to work on any project in this monorepo — from git hooks to
integration tests to E2E tests.

> **Note**: The polyglot demo apps (`a-demo-be-*`, `a-demo-fe-*`) were removed from this repo on
> 2026-04-18. The optional-scope phases below survive for languages this repo may still need; a phase
> with no project in this repo is safe to skip.

**When to use**: new developer onboarding, a fresh machine/OS install, recovering a broken
toolchain, or verifying an environment after adding a new project language.

## Contents

- [Execution Mode](./development-environment-setup/01-execution-mode.md) — manual orchestration.
- [Tool Inventory](./development-environment-setup/02-tool-inventory.md) — all 9 tools table.
- [Quick Start: doctor --fix](./development-environment-setup/03-quick-start-doctor-fix.md) — one-command setup.

### Phases

- [Phase 1: System Package Manager](./development-environment-setup/04-phase-1-system-package-manager.md) — Homebrew/apt.
- [Phase 2: Core Tools](./development-environment-setup/05-phase-2-core-tools.md) — Git, Docker, jq.
- [Phase 3: Node.js Ecosystem](./development-environment-setup/06-phase-3-nodejs-ecosystem.md) — Volta, Node, npm.
- [Phase 4: Go Ecosystem](./development-environment-setup/07-phase-4-go-ecosystem.md) — Go toolchain.
- [Phase 6: Python Ecosystem](./development-environment-setup/08-phase-6-python-ecosystem.md) — full scope only.
- [Phase 7: Rust Ecosystem](./development-environment-setup/09-phase-7-rust-ecosystem.md) — full scope only.
- [Phase 8: Elixir/Erlang Ecosystem](./development-environment-setup/10-phase-8-elixir-erlang-ecosystem.md) — full scope only.
- [Phase 9: .NET Ecosystem](./development-environment-setup/11-phase-9-dotnet-ecosystem.md) — full scope only.
- [Phase 10: Dart/Flutter Ecosystem](./development-environment-setup/12-phase-10-dart-flutter-ecosystem.md) — full scope only.
- [Phase 11: Repository Bootstrap](./development-environment-setup/13-phase-11-repository-bootstrap.md) — clone, install, env, doctor.
- [Phase 12: Playwright Browsers](./development-environment-setup/14-phase-12-playwright-browsers.md) — E2E browser install.
- [Phase 13: Verification](./development-environment-setup/15-phase-13-verification.md) — end-to-end smoke test.

### Reference

- [Termination Criteria](./development-environment-setup/16-termination-criteria.md) — success/partial/failure.
- [Minimal Scope Quick Reference](./development-environment-setup/17-minimal-scope-quick-reference.md) — minimal-scope table.
- [Notes](./development-environment-setup/18-notes.md) — pinning, idempotency, platform notes.
- [Principles Respected](./development-environment-setup/19-principles-implemented-respected.md) — governance.
- [Conventions Respected](./development-environment-setup/20-conventions-implemented-respected.md) — governance.
- [Related Workflows](./development-environment-setup/21-related-workflows.md) — CI Quality Gate.
- [Related Documentation](./development-environment-setup/22-related-documentation.md) — how-to guide, governance docs.
- [Agents](./development-environment-setup/23-agents.md) — repo-rules-checker follow-up.
