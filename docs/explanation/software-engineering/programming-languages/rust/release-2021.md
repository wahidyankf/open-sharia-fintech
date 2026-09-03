---
title: Rust 2021 Edition Release
description: OSE Platform compatibility note for the superseded Rust 2021 edition
category: explanation
subcategory: prog-lang
tags:
  - rust
  - edition
  - release
principles:
  - explicit-over-implicit
  - reproducibility
version: "2021"
lts_until: not-applicable
status: superseded
created: 2026-09-03
---

# Rust 2021 Edition Release

Rust 2021 is the platform's previous edition. Existing crates can interoperate with crates on newer
editions, but new OSE Platform crates must not select it.

Edition selection belongs explicitly in each crate's `Cargo.toml`; toolchain selection remains
separate and is pinned through `rust-toolchain.toml`.

**Upstream reference**: [Rust 2021 migration guide](https://doc.rust-lang.org/edition-guide/rust-2021/index.html)
