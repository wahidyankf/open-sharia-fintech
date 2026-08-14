---
title: "Phase 4: Go Ecosystem (Sequential)"
description: "Phase 4: install Go at the minimum version required by apps/ayokoding-cli/go.mod."
when_to_use: "Use when setting up or verifying the Go toolchain."
---

# Phase 4: Go Ecosystem (Sequential)

Required for Go-based tooling. Note: `ayokoding-cli` and `ose-cli` have migrated to Rust (2026-05-25).

## 5.1 Install Go

```bash
# macOS
brew install go

# Linux — download from https://go.dev/dl/
```

The required minimum version is specified in `apps/ayokoding-cli/go.mod`. As of this writing,
Go >= 1.26.

**Success criteria**: `go version` shows a version >= the go.mod directive.
