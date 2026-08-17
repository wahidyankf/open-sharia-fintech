//! Contract codegen post-processing: Java import cleaning and Dart scaffolding.
//!
//! Backs the `specs clean java-imports` and `specs scaffold dart` commands.
//! Output formatting lives in the command modules themselves
//! (`crate::commands::specs_clean_java_imports`,
//! `crate::commands::specs_scaffold_dart`), matching the rest of the `specs`
//! command family.

pub mod dart_scaffold;
pub mod types;
