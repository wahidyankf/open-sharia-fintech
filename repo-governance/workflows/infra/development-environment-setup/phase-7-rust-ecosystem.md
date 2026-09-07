---
description: "Phase 7 (full scope only): install Rust and cargo-llvm-cov for full Doctor and Rust-content gates."
when_to_use: "Use when satisfying the full Doctor inventory or formatting Rust course content."
---

# Phase 7: Rust Ecosystem (Sequential)

**Condition**: `{input.scope} == full`

Required for: full-scope Doctor verification and Rust course-content formatting gates

This phase runs before the repository bootstrap makes the pinned `./hippo` consumer available. Its
system-level installers therefore remain native and sequential; subsequent repository-local work
uses HIPPO admission.

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
