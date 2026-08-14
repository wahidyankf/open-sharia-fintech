---
title: "When to Revisit This Decision"
description: The conditions under which the native-first toolchain decision should be reconsidered.
category: explanation
subcategory: development
tags:
  - development
  - toolchain
  - doctor
  - environment
  - architecture-decision
created: 2026-04-04
when_to_use: Use when evaluating whether team scale, Docker performance, or contributor needs justify revisiting this decision.
---

# When to Revisit This Decision

Revisit this architectural decision if any of the following conditions change:

- **Team scale**: The team grows to 5+ developers with frequent onboarding, making the setup friction cost significant enough to justify containerization overhead
- **Docker performance**: macOS Docker bind-mount performance reaches native parity, eliminating the primary objection to Dev Containers
- **Cloud development**: A cloud development environment (GitHub Codespaces) becomes necessary for external contributors who cannot install toolchains locally
- **Toolchain count**: The toolchain count exceeds what `rhino-cli doctor` can reasonably manage as a flat list of checks
