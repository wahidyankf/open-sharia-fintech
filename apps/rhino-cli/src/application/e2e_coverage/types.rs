//! Data types for the e2e scenario coverage gap detector.

use std::fs;
use std::path::Path;

use anyhow::{Context, Error};
use serde::{Deserialize, Serialize};

/// A `{feature, scenario}` pair — the key used throughout declared, fixme,
/// and baseline sets.
///
/// Keying on the pair (rather than the scenario title alone) lets scenario
/// titles repeat across different `.feature` files without collision.
#[derive(Debug, Clone, PartialEq, Eq, Hash, PartialOrd, Ord, Serialize, Deserialize)]
pub struct BaselineEntry {
    /// Repo-relative path to the `.feature` file containing the scenario.
    pub feature: String,
    /// Scenario title (without the `Scenario:`/`Scenario Outline:` keyword).
    pub scenario: String,
}

/// The result of diffing a project's current unbound scenarios against its
/// checked-in baseline manifest.
#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub struct GapReport {
    /// Scenarios unbound today (declared ∩ fixme) that the baseline has not
    /// yet accepted — a non-empty set fails the gate. Sorted by
    /// `(feature, scenario)` for deterministic reporting.
    pub new_gaps: Vec<BaselineEntry>,
    /// Baseline entries no longer emitted as `test.fixme` (baseline \
    /// fixme) — never affects `failed`. Two readings of the same computed
    /// set: a previously-unbound scenario that is now bound, and a stale
    /// baseline entry that can be pruned. Sorted by `(feature, scenario)`.
    pub stale: Vec<BaselineEntry>,
    /// `true` when `new_gaps` is non-empty.
    pub failed: bool,
}

/// The checked-in per-project baseline manifest
/// (`e2e-coverage-baseline.json`).
#[derive(Debug, Clone, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct BaselineManifest {
    /// Project name this baseline governs.
    pub project: String,
    /// Scenarios previously accepted as unbound.
    #[serde(rename = "allowedUnbound")]
    pub allowed_unbound: Vec<BaselineEntry>,
}

/// Loads a baseline manifest from `path`.
///
/// Returns an empty manifest (no allowed-unbound entries) when `path` does
/// not exist — the "no baseline manifest yet" case (AC-6's first-time
/// generation scenario).
///
/// # Errors
///
/// Returns an error if `path` exists but cannot be read or parsed as JSON.
pub fn load_baseline(path: &Path) -> Result<BaselineManifest, Error> {
    if !path.exists() {
        return Ok(BaselineManifest::default());
    }
    let content = fs::read_to_string(path)
        .with_context(|| format!("failed to read baseline manifest {}", path.display()))?;
    serde_json::from_str(&content)
        .with_context(|| format!("failed to parse baseline manifest {}", path.display()))
}

/// Serializes `manifest` as pretty-printed JSON and writes it to `path`.
///
/// # Errors
///
/// Returns an error if serialization fails or `path` cannot be written.
pub fn save_baseline(path: &Path, manifest: &BaselineManifest) -> Result<(), Error> {
    let json = serde_json::to_string_pretty(manifest)?;
    fs::write(path, format!("{json}\n"))
        .with_context(|| format!("failed to write baseline manifest {}", path.display()))
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;
    use tempfile::TempDir;

    #[test]
    fn load_baseline_returns_empty_manifest_when_missing() {
        let tmp = TempDir::new().unwrap();
        let path = tmp.path().join("no-such-baseline.json");
        let manifest = load_baseline(&path).unwrap();
        assert!(manifest.allowed_unbound.is_empty());
    }

    #[test]
    fn save_then_load_baseline_round_trips() {
        let tmp = TempDir::new().unwrap();
        let path = tmp.path().join("baseline.json");
        let manifest = BaselineManifest {
            project: "example-e2e".to_string(),
            allowed_unbound: vec![BaselineEntry {
                feature: "specs/x.feature".to_string(),
                scenario: "A".to_string(),
            }],
        };
        save_baseline(&path, &manifest).unwrap();
        let loaded = load_baseline(&path).unwrap();
        assert_eq!(loaded, manifest);
    }
}
