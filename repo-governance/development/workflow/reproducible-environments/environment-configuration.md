---
title: "Environment Configuration"
description: Summary pointer to the .env template pattern, the no-secrets-in-git iron rule, and the env backup/restore toolchain.
category: explanation
subcategory: development
tags:
  - development
  - reproducibility
  - volta
  - docker
  - environment
  - dependencies
created: 2025-12-28
when_to_use: Use when locating the full env/secrets standards, or recalling the .env.example pattern and backup/restore commands.
---

# Environment Configuration

> **Stub.** The full env/secrets standards — naming convention, annotation format, `.env.example`
> layout, startup validation, `rhino-cli env` toolchain, and drift guard — live in
> [`secrets-and-env-standards.md`](../../../conventions/security/secrets-and-env-standards.md).

## .env Files (summary)

**Pattern**: Committed template (`apps/<app>/.env.example`), gitignored real file (`.env.local`).

**Hard iron rule**: Real secret values never enter git. `.env.example` (committed template) contains
placeholders only. See:
[`secrets-and-env-standards.md` § 1](../../../conventions/security/secrets-and-env-standards/hard-iron-rule-no-secrets-in-committed-files.md#hard-iron-rule--no-secrets-in-committed-files).

**Backup and restore**: Use `rhino-cli env backup / restore`. See:
[`secrets-and-env-standards.md` § 6](../../../conventions/security/secrets-and-env-standards/rhino-cli-env-toolchain.md#rhino-cli-env-toolchain).
