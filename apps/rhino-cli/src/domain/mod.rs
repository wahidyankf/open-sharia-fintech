//! Pure domain types and business rules — no I/O.

/// CLI output format enum (`text`, `json`, `markdown`).
pub mod cliout;
/// Pure git-domain helpers (staged-file filters).
pub mod git;
/// Mermaid diagram parsing and validation domain model.
pub mod mermaid;

/// Standard-stream descriptor-flag hygiene for git-hook invocations.
pub mod stdio_blocking;
