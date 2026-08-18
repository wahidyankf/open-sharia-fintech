---
title: "Implementation Notes"
description: The shell-restart caveat after installing a version manager, --dry-run preview mode, and the idempotency contract for doctor --fix install commands.
category: explanation
subcategory: development
tags:
  - development
  - toolchain
  - doctor
  - environment
  - architecture-decision
created: 2026-04-04
when_to_use: Use when implementing or debugging a doctor --fix install command.
---

# Implementation Notes

## Shell Restart Caveat

Volta, SDKMAN, and rustup modify shell profile files. After installing any of these tools, the fixer must `source` the relevant init script before installing dependent tools:

```bash
# After Volta install
source ~/.zshrc  # Or detect shell dynamically

# After SDKMAN install
source "$HOME/.sdkman/bin/sdkman-init.sh"

# After rustup install
source "$HOME/.cargo/env"
```

## `--dry-run` Mode

`doctor --fix --dry-run` prints what would be installed without executing. This preview capability gives developers confidence before applying changes, equivalent to reviewing a Terraform plan before applying.

## Idempotency Contract

When implementing `doctor --fix`, each install command must be non-interactive and idempotent. The table in the Rationale section documents the re-run behavior of each package manager. Pay particular attention to `rustup`, which requires the `-y` flag for non-interactive mode, and Flutter, which requires `brew install --cask flutter` rather than `brew install flutter`.
