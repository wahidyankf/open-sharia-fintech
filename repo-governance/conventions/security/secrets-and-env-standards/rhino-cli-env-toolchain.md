---
title: "`rhino-cli env` Toolchain"
description: The rhino-cli env command family (backup, restore, init, validate), the backup-scope registry, and the env-contract section that drives drift validation.
when_to_use: Use when running or configuring rhino-cli env backup/restore/init/validate, or when adding a new surface to the env-contract registry.
category: explanation
subcategory: conventions
tags:
  - security
  - secrets
  - env-files
  - guard-env-file-access
  - naming
  - reproducibility
created: 2026-06-10
---

# `rhino-cli env` Toolchain

The full `rhino-cli env` family manages the local secrets lifecycle:

| Command                             | What it does                                                                       |
| ----------------------------------- | ---------------------------------------------------------------------------------- |
| `rhino-cli env backup [--dry-run]`  | Copies all secret files to `~/<repo-name>-env-backup/`                             |
| `rhino-cli env restore [--dry-run]` | Restores from the backup directory                                                 |
| `rhino-cli env init`                | Scaffolds `.env.local` from every `apps/<app>/.env.example` template               |
| `rhino-cli env validate`            | Checks each surface in `env-contract:` (`repo-config.yml`) for code↔template drift |

## Backup scope — hybrid floor + registry

Backup coverage = hardcoded floor ∪ `backup_globs` from the `env-contract:` section in `repo-config.yml`:

| Pattern                      | Status                                                  |
| ---------------------------- | ------------------------------------------------------- |
| `.env`, `.env.*`             | active                                                  |
| Everything under `.secrets/` | active                                                  |
| `secrets.json` at repo root  | active                                                  |
| `*.tfvars`, `*.tfvars.json`  | commented forward-scaffold — activate when IaC is added |
| Generated inventories        | commented forward-scaffold — activate when IaC is added |

The default backup target is `~/<repo-root-basename>-env-backup/` (e.g. `~/ose-public-env-backup/`).
This is the canonical per-repo backup directory aligned across the ose-public/ose-private
sibling repos.

## `env-contract:` section and drift validation

The `env-contract:` section in `repo-config.yml` at repo root declares each surface to validate:

```yaml
env-contract:
  surfaces:
    - root: apps/organiclever-be
      kind: app
      lang: rust
      allowlist: []
    - root: apps/ose-www
      kind: app
      lang: typescript
      allowlist: [PORT, HOSTNAME]
    # Terraform/Ansible: forward-scaffold — activate when IaC is added
```

`rhino-cli env validate` compares declared keys in `.env.example` against read keys in source code,
reporting `declared-but-unread` (stale template entry) and `read-but-undeclared` (undocumented read)
drift findings. Invoked by `.husky/pre-push` and `.github/workflows/validate-env.yml`.
