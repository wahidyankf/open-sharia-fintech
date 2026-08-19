# Rust Quick Standards — Unsafe Policy, Cargo.toml, Clippy/rustfmt

## Unsafe Code Policy (MANDATORY)

**MUST** forbid unsafe code in **both** `lib.rs` and `main.rs` — the attribute is not inherited between targets:

```rust
// src/lib.rs — line 1
#![forbid(unsafe_code)]

// src/main.rs — line 1
#![forbid(unsafe_code)]
```

**MUST** also encode at manifest level in `Cargo.toml`:

```toml
[lints.rust]
unsafe_code = "forbid"
```

Infrastructure crates requiring `unsafe` MUST include a `// SAFETY:` comment on every `unsafe` block.

**See**: [Code Quality Standards §Unsafe Code Policy](../../../docs/explanation/software-engineering/programming-languages/rust/code-quality-standards.md#unsafe-code-policy)

## Cargo.toml Required Structure

**MUST** declare `edition`, `rust-version`, and `[lints.rust]`. **MUST** configure release profile with LTO and `panic = "abort"`:

```toml
[package]
name = "my-crate"
version = "0.1.0"
edition = "2024"
rust-version = "1.88"   # MSRV — minimum compiler to build this crate

[lints.rust]
unsafe_code = "forbid"

[profile.release]
opt-level = 3
lto = "thin"
codegen-units = 1
panic = "abort"   # smaller binary, no unwinding tables
strip = "symbols"
```

`rust-version` (MSRV) ≠ `channel` in `rust-toolchain.toml` (installed toolchain). Installed ≥ MSRV is the invariant.

**See**: [Build Configuration](../../../docs/explanation/software-engineering/programming-languages/rust/build-configuration.md)

## Clippy and rustfmt (MANDATORY)

```toml
# .rustfmt.toml
edition = "2024"
max_width = 100
use_small_heuristics = "Default"
reorder_imports = true
reorder_modules = true
```

Configure Clippy via `[lints.clippy]` in `Cargo.toml` (not CLI flags) — checked into source
control, applies consistently across contributors and CI:

```toml
# Cargo.toml
[lints.clippy]
# Enable pedantic at low priority — per-lint allows below override at default priority 0
pedantic = { level = "warn", priority = -1 }

# --- Documented allows (document the why for each) ---
must_use_candidate = "allow"
missing_errors_doc = "allow"

# --- Restriction lints: hard errors even without -D warnings ---
unwrap_used = "deny"
panic = "deny"
undocumented_unsafe_blocks = "deny"
```

```bash
# Run before commit
cargo fmt --check                    # Check formatting
cargo clippy --all-targets -- -D warnings  # Fail on any warning (lints from Cargo.toml)
cargo test                           # Run all tests
```
