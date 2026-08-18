---
title: "Principles and Conventions Implemented"
description: The principles and companion conventions the Dependency Bump Stability & Safety Policy implements and respects.
category: explanation
subcategory: development
tags:
  - dependencies
  - security
  - versioning
  - reproducibility
  - workflow
created: 2026-05-15
when_to_use: Use when tracing why the three-path decision tree and exact-pinning rules exist back to the principles and conventions they respect.
---

# Principles and Conventions Implemented

## Principles Implemented/Respected

This practice implements/respects the following core principles:

- **[Reproducibility First](../../../principles/software-engineering/reproducibility.md)**: All version specifications use exact pins — no caret, no tilde, no `latest`. Lockfiles are the sole source of truth for the resolved graph. Deterministic installs on every machine and CI runner.

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**: Every version is stated explicitly in manifests. Path classification (LTS / 60-day / waiver) is documented in writing. Cutoff dates are computed and recorded. No version is ever implicitly "latest".

- **[Automation Over Manual](../../../principles/software-engineering/automation-over-manual.md)**: Verification commands (`grep`, `npm audit`, `govulncheck`, lockfile update commands) are prescribed steps in the application workflow so that correctness checks run mechanically rather than relying on reviewer memory.

- **[Root Cause Orientation](../../../principles/general/root-cause-orientation.md)**: When a package has a CVE, the fix is to upgrade to the patched version (root cause resolved) rather than suppressing the audit warning or adding an exception comment.

- **[Deliberate Problem-Solving](../../../principles/general/deliberate-problem-solving.md)**: The three-path decision tree forces explicit classification before a version is chosen. Engineers and agents state their reasoning in writing rather than picking the newest available tag reflexively.

## Conventions Implemented/Respected

This practice respects the following conventions:

- **[Reproducible Environments Convention](../reproducible-environments.md)**: Exact version pinning in `package.json`, Volta block, `go.mod`, `global.json`, `rust-toolchain.toml`, `.tool-versions`, and Dockerfiles directly implements the reproducibility standards established there.

- **[Commit Message Convention](../commit-messages.md)**: Dependency bump commits use `chore(deps): bump <package> to <version>` or `fix(deps): patch CVE-YYYY-NNNNN in <package>` per Conventional Commits format.
