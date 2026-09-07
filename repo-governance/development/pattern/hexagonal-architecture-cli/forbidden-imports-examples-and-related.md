---
description: "The forbidden-imports table, a worked Rust example of a command delegating to the application layer, and related pattern documentation."
when_to_use: "Use when checking whether a CLI layer imports something forbidden, or want a worked example of the commands/ to application/ handoff."
---

# Forbidden Imports, Examples, and Related

## Forbidden Imports

| Layer             | Forbidden                                                                           |
| ----------------- | ----------------------------------------------------------------------------------- |
| `domain/`         | `clap`, `cobra`, any HTTP framework, any DB driver, `std::io` (Rust stdout)         |
| `application/`    | `clap`, `cobra`, concrete infrastructure types, HTTP framework types                |
| `infrastructure/` | `clap`, `cobra`, business logic — push invariants to `domain/`                      |
| `commands/`       | Direct database drivers, external HTTP SDKs (must use ports through `application/`) |

## Examples

A Rust CLI command delegating to the application layer:

```rust
// src/commands/validate.rs  (inbound adapter — Clap lives here)
use clap::Args;
use crate::application::validate_links::{ValidateLinksInput, validate_links};

#[derive(Args)]
pub struct ValidateArgs {
    /// Root directory to scan
    pub root: std::path::PathBuf,
    /// Fail on the first broken link
    #[arg(long)]
    pub fail_fast: bool,
}

pub fn run(args: ValidateArgs) -> anyhow::Result<()> {
    // Translate CLI args to application input type
    let input = ValidateLinksInput {
        root: args.root,
        fail_fast: args.fail_fast,
    };

    // Call application layer — no Clap types cross this boundary
    let result = validate_links(input)?;

    // Print results (side effect confined to commands/)
    for broken in &result.broken_links {
        eprintln!("BROKEN: {broken}");
    }

    if !result.broken_links.is_empty() {
        std::process::exit(1);
    }
    Ok(())
}
```

```rust
// src/application/validate_links.rs  (application layer — no Clap import)
use crate::domain::link::Link;

pub struct ValidateLinksInput {
    pub root: std::path::PathBuf,
    pub fail_fast: bool,
}

pub struct ValidateLinksOutput {
    pub broken_links: Vec<Link>,
}

pub fn validate_links(input: ValidateLinksInput) -> Result<ValidateLinksOutput, crate::application::AppError> {
    // Orchestrates domain + outbound ports; no Clap types visible here
    todo!()
}
```

## Related

- **[Hexagonal Architecture](../hexagonal-architecture.md)** — Core pattern, dependency rule, and layer definitions
