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

`apps/rhino-cli` is the repository's only Rust project. It uses
[Clippy](https://github.com/rust-lang/rust-clippy) for static analysis.

**Configuration**: the project declares its lints in `Cargo.toml` under `[lints.clippy]`, using the
pedantic profile with selective allows.

**Standard lint set** (from `apps/rhino-cli/Cargo.toml`):

- `pedantic` at `warn` priority -1 (baseline)
- `unwrap_used = "deny"` — no `.unwrap()` in production code
- `panic = "deny"` — no `panic!()` in production code
- `missing_docs = "deny"` / `missing_docs_in_private_items = "deny"` — full doc coverage
- `undocumented_unsafe_blocks = "deny"` — every `unsafe` block must have a comment
- `unsafe_code = "forbid"` (in `[lints.rust]`) — no unsafe code at all

**Usage**:

```bash
# Run via Nx (standard)
nx run rhino-cli:lint

# Run directly
cargo clippy --manifest-path apps/rhino-cli/Cargo.toml --all-targets -- -D warnings
```

Other backends are linted by their own language toolchains, not Clippy — `organiclever-be` and
`ose-be` are F#, and use the F# analyzers described in this directory's formatter and hook
documents.
