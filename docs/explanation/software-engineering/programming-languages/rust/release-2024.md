---
title: Rust 2024 Edition Release
description: OSE Platform compatibility note for the required Rust 2024 edition
category: explanation
subcategory: prog-lang
tags:
  - rust
  - edition
  - release
principles:
  - explicit-over-implicit
  - reproducibility
version: "2024"
lts_until: not-applicable
status: current
created: 2026-09-03
---

# Rust 2024 Edition Release

Rust 2024 is the required edition for OSE Platform crates. Declare `edition = "2024"` in
`Cargo.toml`; do not infer the edition from whichever compiler happens to be installed.

Use `cargo fix --edition` when migrating and verify the resulting code before changing the manifest.
The repository's pinned toolchain must be new enough to support the edition.

**Upstream reference**: [Rust 2024 migration guide](https://doc.rust-lang.org/edition-guide/rust-2024/index.html)
