---
title: "Rust CLI Linting"
description: "How Rust CLI code (rhino-cli) is linted."
category: explanation
subcategory: development
tags:
  - development
  - code-quality
  - prettier
  - husky
  - lint-staged
  - git-hooks
  - automation
created: 2026-05-12
when_to_use: "Use when configuring or debugging Rust CLI lint gates."
---

# Rust CLI Linting

Rust CLI projects (`apps/ayokoding-cli`, `apps/ose-cli`, `apps/rhino-cli`) use [Clippy](https://github.com/rust-lang/rust-clippy) for static analysis.

**Configuration**: Each project declares lints in its `Cargo.toml` under `[lints.clippy]`. The standard pedantic profile is used with selective allows.

**Standard lint set** (from each project's `Cargo.toml`):

- `pedantic` at `warn` priority -1 (baseline)
- `unwrap_used = "deny"` — no `.unwrap()` in production code
- `panic = "deny"` — no `panic!()` in production code
- `missing_docs = "deny"` / `missing_docs_in_private_items = "deny"` — full doc coverage
- `undocumented_unsafe_blocks = "deny"` — every `unsafe` block must have a comment
- `unsafe_code = "forbid"` (in `[lints.rust]`) — no unsafe code at all

**Usage**:

```bash
# Run via Nx (standard)
nx lint ayokoding-cli
nx lint ose-cli
nx lint organiclever-be

# Run directly
cargo clippy --manifest-path apps/ayokoding-cli/Cargo.toml --all-targets -- -D warnings
```
