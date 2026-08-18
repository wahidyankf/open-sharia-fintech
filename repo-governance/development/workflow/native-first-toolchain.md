---
title: "Native-First Toolchain Management"
description: Architectural decision to use native package managers and rhino-cli doctor instead of Terraform, Ansible, or Dev Containers.
category: explanation
subcategory: development
tags:
  - development
  - toolchain
  - doctor
  - environment
  - architecture-decision
created: 2026-04-04
when_to_use: Use when deciding how to install or verify a toolchain, or evaluating Terraform, Ansible, or Docker Dev Containers.
---

# Native-First Toolchain Management

This document records the architectural decision to use native toolchain management (`rhino-cli doctor` and package managers) instead of infrastructure-as-code tools (Terraform, Ansible, Docker Dev Containers) for development environment setup. The open-sharia-enterprise monorepo spans multiple toolchains (Node.js, Rust, .NET/F#), making toolchain management a significant architectural concern.

## Contents

- [Principles, Conventions, Context, and Decision](./native-first-toolchain/principles-conventions-context-and-decision.md) — Why native management, and the decision itself.
- [Rationale — Package Managers Through Docker Performance](./native-first-toolchain/rationale-package-managers-through-docker-performance.md) — Idempotency, source of truth, single-machine scope, and Docker's macOS cost.
- [Rationale — Worktrees and the Doctor Pattern](./native-first-toolchain/rationale-worktrees-and-the-doctor-pattern.md) — Worktree incompatibility with containers, the doctor check-diff-apply mapping, and future-decision guidance.
- [Platform Support and Git Worktree Compatibility](./native-first-toolchain/platform-support-and-git-worktree-compatibility.md) — macOS/Ubuntu support and worktree-safe path resolution.
- [Implementation Notes](./native-first-toolchain/implementation-notes.md) — Shell-restart caveat, `--dry-run` mode, and the idempotency contract.
- [When to Revisit This Decision](./native-first-toolchain/when-to-revisit-this-decision.md) — The conditions that would change this decision.

## Related Documentation

- [Reproducible Environments](../workflow/reproducible-environments.md) — broader reproducibility practices (Volta, lockfiles, Docker for services).
- [Development Environment Setup](../../workflows/infra/development-environment-setup.md) — workflow for setting up a development environment.
- [Native Dev Setup Improvements Plan](../../../plans/done/2026-04-04__native-dev-setup-improvements/README.md) — completed plan that implemented `doctor --fix` and related improvements.
