//! `specs e2e-coverage validate` — detects Gherkin scenarios that
//! playwright-bdd's `missingSteps: "skip-scenario"` setting silently converts
//! to `test.fixme(...)` in generated `.spec.js` output.
//!
//! A checked-in per-project baseline manifest lists scenarios already known
//! to be unbound, so only *new* unbound scenarios beyond the baseline fail
//! the gate. See `docs/reference/sdlc-gate-standard.md` and the
//! `e2e-scenario-coverage-gap-detector` plan's `tech-docs.md` for the full
//! design rationale.

/// Pure diff core: computes new/stale gaps between declared, fixme, and
/// baseline scenario sets.
pub mod diff;
/// Declared-scenario extraction (`@e2e` filter) and generated-output
/// scanning (`test.fixme` title extraction).
pub mod parser;
/// Text/JSON/Markdown formatters for [`types::GapReport`].
pub mod reporter;
/// Data types: [`types::BaselineEntry`] and [`types::GapReport`].
pub mod types;
