---
title: "Rust Code Quality Standards"
description: Authoritative OSE Platform Rust code quality standards (rustfmt, Clippy, cargo audit, unsafe policy)
category: explanation
subcategory: prog-lang
tags:
  - rust
  - code-quality
  - clippy
  - rustfmt
  - cargo-audit
  - unsafe
principles:
  - automation-over-manual
  - explicit-over-implicit
  - immutability
  - pure-functions
  - reproducibility
created: 2026-03-09
---

# Rust Code Quality Standards

## Prerequisite Knowledge

**REQUIRED**: You MUST understand Rust fundamentals from [AyoKoding Rust Learning Path](../../../../../apps/ayokoding-www/content/en/learn/legacy/software-engineering/programming-languages/rust/_index.md) before using these standards.

**This document is OSE Platform-specific**, not a Rust tutorial.

**See**: [Programming Language Documentation Separation Convention](../../../../../repo-governance/conventions/structure/programming-language-docs-separation.md)

## Purpose

This document defines **authoritative code quality standards** for Rust development in the OSE Platform. All Rust projects MUST meet these quality requirements before code review approval.

**Target Audience**: OSE Platform Rust developers, CI/CD pipeline maintainers, technical reviewers

**Scope**: rustfmt configuration, Clippy lint set, cargo audit, cargo deny, unsafe code policy

## Software Engineering Principles

### 1. Automation Over Manual

Quality enforcement MUST be automated:

- rustfmt runs on pre-commit (never manual formatting decisions)
- Clippy runs in CI with `--deny warnings` (zero tolerance for lint warnings)
- cargo audit runs in CI on every push (automated CVE detection)
- cargo deny runs in CI (automated license and policy enforcement)

### 2. Explicit Over Implicit

Quality standards are explicit:

- `.rustfmt.toml` documents all formatting decisions
- `deny.toml` documents all dependency policies
- `unsafe` blocks document SAFETY invariants inline

### 3. Immutability Over Mutability

Clippy's `clippy::pedantic` lint group catches unnecessary mutation:

- `clippy::needless_pass_by_value` — suggests borrowing where ownership not needed
- `clippy::redundant_closure` — detects closures that wrap functions

## rustfmt Configuration

**MUST** use rustfmt for all Rust code. rustfmt is non-negotiable — all formatting disputes are resolved by the formatter.

**MUST** configure rustfmt via `.rustfmt.toml` at the workspace root:

```toml
# .rustfmt.toml
edition = "2024"
max_width = 100
use_small_heuristics = "Default"
reorder_imports = true
reorder_modules = true
```

**Enforce on pre-commit**:

```bash
# Check formatting (used in CI)
cargo fmt --all -- --check

# Apply formatting (used in pre-commit hook)
cargo fmt --all
```

**MUST NOT** use `#[rustfmt::skip]` except for macro invocations or alignment-critical code with a documented justification.

## Clippy Configuration

**MUST** run Clippy with at minimum the `clippy::pedantic` lint group. All warnings are treated as errors in CI.

### Clippy Invocation

```bash
# CI invocation — denies all warnings (lints configured in Cargo.toml)
cargo clippy --all-targets -- -D warnings
```

### Cargo.toml Clippy Configuration

**MUST** configure Clippy in `Cargo.toml` via `[lints.clippy]`. This is preferred over CLI flags because
it is checked into source control, applies consistently across all contributors and CI, and allows
per-lint overrides with priority ordering.

```toml
# Cargo.toml
[lints.clippy]
# Enable pedantic group at low priority — individual allows below override via priority 0
pedantic = { level = "warn", priority = -1 }

# --- Documented allows ---
must_use_candidate = "allow"
missing_errors_doc = "allow"
missing_panics_doc = "allow"

# --- Restriction lints (hard errors, cannot be suppressed by -D warnings alone) ---
unwrap_used = "deny"
panic = "deny"
undocumented_unsafe_blocks = "deny"
```

**Key config decisions**:

- `pedantic = { level = "warn", priority = -1 }` — enables the group at lower priority so per-lint
  `"allow"` or `"deny"` entries (which default to priority 0) take precedence without needing
  `priority` on every override
- Restriction lints set to `"deny"` become hard errors even without `-D warnings`; they cannot be
  silenced by `--cap-lints warn`

### Key Clippy Lints (MUST address)

| Lint                              | Severity | Description                                |
| --------------------------------- | -------- | ------------------------------------------ |
| `clippy::unwrap_used`             | DENY     | Forbid `unwrap()` in production code       |
| `clippy::expect_used`             | WARN     | Warn on `expect()` — document invariant    |
| `clippy::panic`                   | DENY     | Forbid panic in library code               |
| `clippy::indexing_slicing`        | WARN     | Prefer `get()` over direct indexing        |
| `clippy::arithmetic_side_effects` | WARN     | Prefer checked arithmetic in domain logic  |
| `clippy::float_arithmetic`        | DENY     | Forbid float in financial calculations     |
| `clippy::clone_on_ref_ptr`        | DENY     | Explicit `Arc::clone(&x)` over `x.clone()` |

### Suppressing Lints (Requires Justification)

**MUST** document the reason when suppressing a lint:

```rust
// CORRECT: Documented suppression
// The complexity here is inherent to the validation algorithm.
// Extracting sub-functions would obscure the logical flow.
#[allow(clippy::cognitive_complexity)]
fn validate_murabaha_contract(contract: &MurabahaContract) -> Result<(), Vec<ValidationError>> {
    ...
}

// WRONG: Silent suppression without reason
#[allow(clippy::too_many_arguments)]
fn process_contract(...) { ... }
```

## deny(warnings) in CI

**MUST** compile with `-D warnings` in CI environments.

```bash
# CI build command
RUSTFLAGS="-D warnings" cargo build --all-targets --all-features
```

**MUST** configure in workspace `Cargo.toml` for local development:

```toml
# Cargo.toml
[profile.dev]
# Warnings become errors in development too
# (can be relaxed during active prototyping)
```

## cargo audit for Security Vulnerabilities

**MUST** run `cargo audit` in CI to detect known CVEs in dependencies.

```bash
# Install
cargo install cargo-audit

# Run audit
cargo audit

# Fail CI on any vulnerability
cargo audit --deny warnings
```

**MUST** configure `audit.toml` to manage known/accepted advisories:

```toml
# audit.toml
[advisories]
# Example: ignore a specific advisory with justification
ignore = [
    # RUSTSEC-2021-0001: vulnerability in foo crate
    # Status: No fix available; mitigated by [describe mitigation]
    # Review due: 2026-06-01
    "RUSTSEC-2021-0001",
]
```

## cargo deny for Dependency Policy

**MUST** configure `cargo deny` with a `deny.toml` file at the workspace root to enforce:

- License allowlist (only approved licenses)
- Banned crates
- Duplicate version limits

```toml
# deny.toml
[licenses]
allow = [
    "MIT",
    "Apache-2.0",
    "Apache-2.0 WITH LLVM-exception",
    "BSD-2-Clause",
    "BSD-3-Clause",
    "ISC",
    "Unicode-DFS-2016",
]
deny = [
    "GPL-2.0",
    "GPL-3.0",
    "LGPL-2.0",
    "LGPL-2.1",
]

[bans]
multiple-versions = "warn"
deny = [
    # Use rustls instead
    { name = "openssl" },
    { name = "openssl-sys" },
]

[advisories]
db-path = "~/.cargo/advisory-db"
db-urls = ["https://github.com/rustsec/advisory-db"]
```

## Unsafe Code Policy

**MUST** apply `#![forbid(unsafe_code)]` to all application crates. Unsafe code is only permitted in infrastructure crates with documented justification.

```rust
// CORRECT: Application code forbids unsafe
#![forbid(unsafe_code)]

// lib.rs for application crate
pub mod domain;
pub mod application;
pub mod infrastructure;
```

**MUST** include `#![forbid(unsafe_code)]` in **both** `lib.rs` and `main.rs` when a crate exposes both a library target and a binary target. The attribute is not inherited between targets — omitting it from one root silently permits unsafe in that target.

```rust
// CORRECT: Both crate roots forbid unsafe
// src/lib.rs — line 1
#![forbid(unsafe_code)]

// src/main.rs — line 1
#![forbid(unsafe_code)]
```

**MUST** include a `// SAFETY:` comment on every `unsafe` block in infrastructure crates:

```rust
// CORRECT: Documented unsafe block
// SAFETY: The pointer is non-null and aligned because it was returned
// by Box::into_raw() on line 42, and has not been aliased since.
let value = unsafe { Box::from_raw(ptr) };

// WRONG: Undocumented unsafe block
let value = unsafe { Box::from_raw(ptr) }; // No SAFETY comment
```

**MUST** use `unsafe` in the narrowest possible scope:

```rust
// CORRECT: Minimal unsafe scope
let result = {
    // SAFETY: ptr is guaranteed valid for the lifetime of this block
    let ptr_value = unsafe { *ptr };
    ptr_value * 2 // Safe arithmetic outside unsafe block
};

// WRONG: Unnecessary expansion of unsafe scope
let result = unsafe {
    let ptr_value = *ptr;
    ptr_value * 2 // Arithmetic does not need to be unsafe
};
```

## Enforcement

**CI Pipeline (REQUIRED)**:

```yaml
# Required CI steps for all Rust projects
- cargo fmt --all -- --check
- RUSTFLAGS="-D warnings" cargo build --all-targets
- cargo clippy --all-targets -- -D warnings -D clippy::pedantic
- cargo test --all-targets
- cargo audit
- cargo deny check
```

**Pre-commit checklist**:

- [ ] `cargo fmt` applied (no formatting changes)
- [ ] `cargo clippy` passes with zero warnings
- [ ] No `unsafe` blocks without `// SAFETY:` comments
- [ ] No `#[allow(...)]` without documented reason
- [ ] `cargo audit` passes (no known vulnerabilities)
- [ ] No banned licenses or crates (cargo deny)

## Related Standards

- [Security Standards](security-standards.md) - cargo audit, secrets management
- [Build Configuration](build-configuration.md) - Cargo.toml, CI integration
- [Coding Standards](coding-standards.md) - Naming and idioms

## Related Documentation

**Software Engineering Principles**:

- [Automation Over Manual](../../../../../repo-governance/principles/software-engineering/automation-over-manual.md)
- [Explicit Over Implicit](../../../../../repo-governance/principles/software-engineering/explicit-over-implicit.md)

---

**Maintainers**: Platform Documentation Team

**Rust Version**: MSRV declared via the crate's `rust-version` field in `Cargo.toml`; Edition 2024
