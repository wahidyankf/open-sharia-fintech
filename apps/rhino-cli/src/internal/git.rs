//! Backward-compatibility re-exports for the `git` feature.
//!
//! The implementation now lives in `crate::application::git` and
//! `crate::infrastructure::git`. This module keeps existing callers
//! working during the incremental hexagonal migration.

/// Git repository root locator (re-exported from `infrastructure::git::root`).
pub mod root;
