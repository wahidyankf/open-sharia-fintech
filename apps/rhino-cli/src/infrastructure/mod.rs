//! Infrastructure adapters — I/O, reporters, and file-system helpers.

/// Filesystem infrastructure adapters (the real `Fs` implementation).
pub mod fs;
/// Git infrastructure adapters (root finder + staged-file provider).
pub mod git;
/// Mermaid infrastructure adapters (extractor + reporter).
pub mod mermaid;
/// Standard-stream descriptor-flag hygiene for git-hook invocations.
pub mod stdio_blocking;
