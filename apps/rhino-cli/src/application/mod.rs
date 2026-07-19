//! Application use cases and port definitions.

/// Agent validation, sync, conversion, and binding use cases.
pub mod agents;
/// Bounded-context registry loader and validator.
pub mod bcregistry;
/// Per-level @covers behavior coverage engine.
pub mod behavior_coverage;
/// Documentation validation use cases.
pub mod docs;
/// Doctor (toolchain-check) use case.
pub mod doctor;
/// `specs domain-coverage validate` — behavior coverage scoped to domain/** feature files.
pub mod domain_coverage;
/// `specs e2e-coverage validate` — playwright-bdd `test.fixme` baseline gap detector.
pub mod e2e_coverage;
/// Environment-file use cases (backup, validate).
pub mod env;
/// Filesystem I/O use cases and port definitions.
pub mod fs;
/// Git pre-commit use cases and port definitions.
pub mod git;
/// Glossary validator use case.
pub mod glossary;
/// Mermaid validation use cases and extractor port.
pub mod mermaid;
/// Agent and workflow naming convention validators.
pub mod naming;
/// Unified repo-config.yml loader.
pub mod repo_config;
/// Repository governance audit use cases.
pub mod repo_governance;
/// Severity level enum and resolution helpers.
pub mod severity;
/// Spec-coverage validation use cases.
pub mod speccoverage;
/// Spec-tree validators.
pub mod specs;
/// Test-coverage subsystem: parsers (LCOV/JaCoCo/Cobertura/Go), diff, merge, and reporters.
pub mod testcoverage;
