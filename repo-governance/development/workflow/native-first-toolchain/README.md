---
title: "Native-First Toolchain Management"
description: "Architectural decision to use native package managers and rhino-cli doctor instead of Terraform, Ansible, or Dev Containers."
when_to_use: "Read this index to find the right Native-First Toolchain Management child document."
---

# Native-First Toolchain Management

- [Principles, Conventions, Context, and Decision](./01-principles-conventions-context-and-decision.md) — The principles and conventions native-first toolchain management implements, the context that prompted the decision, and the decision itself. Use when tracing why native toolchain management was chosen over Terraform, Ansible, or Docker Dev Containers.
- [Rationale — Package Managers Through Docker Performance](./02-rationale-package-managers-through-docker-performance.md) — Why native package managers are already idempotent, why installed binaries are the source of truth, why this is a single-machine problem, and why Docker Dev Containers cost too much on macOS. Use when justifying why native toolchain management beats IaC or containerized dev environments for this monorepo.
- [Rationale — Worktrees and the Doctor Pattern](./03-rationale-worktrees-and-the-doctor-pattern.md) — Why Docker Dev Containers are incompatible with git worktree isolation, how rhino-cli doctor mirrors the IaC check-diff-apply pattern, and guidance for future toolchain decisions. Use when justifying the doctor-based check-diff-apply pattern, or when deciding whether a new tool fits native-first management.
- [Platform Support and Git Worktree Compatibility](./04-platform-support-and-git-worktree-compatibility.md) — Which platforms doctor --fix supports and how, and why every command already works correctly from a git worktree. Use when setting up doctor on Ubuntu/Linux, or when confirming toolchain commands are worktree-safe.
- [Implementation Notes](./05-implementation-notes.md) — The shell-restart caveat after installing a version manager, --dry-run preview mode, and the idempotency contract for doctor --fix install commands. Use when implementing or debugging a doctor --fix install command.
- [When to Revisit This Decision](./06-when-to-revisit-this-decision.md) — The conditions under which the native-first toolchain decision should be reconsidered. Use when evaluating whether team scale, Docker performance, or contributor needs justify revisiting this decision.
