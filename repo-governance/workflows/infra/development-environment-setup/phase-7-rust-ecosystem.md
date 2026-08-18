---
title: "Phase 7: Rust Ecosystem (Sequential)"
description: "Phase 7 (full scope only): install Rust via rustup and cargo-llvm-cov, required for rhino-cli."
when_to_use: "Use when setting up the Rust toolchain for rhino-cli."
---

# Phase 7: Rust Ecosystem (Sequential)

**Condition**: `{input.scope} == full`

Required for: `rhino-cli`

## 7.1 Install Rust via rustup

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source "$HOME/.cargo/env"
```

**Success criteria**: `rustc --version` returns a version string.

## 7.2 Install cargo-llvm-cov (coverage tool)

```bash
cargo install cargo-llvm-cov
```

**Success criteria**: `cargo llvm-cov --version` returns a version string.
