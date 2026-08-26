/// File IO, process spawn, and git helpers land here wave by wave, mirroring
/// the Rust `infrastructure/` module tree. Phase 2 seeds an empty module so
/// the project builds and later waves have a namespace to add to rather than
/// creating one under review pressure.
///
/// Deliberately no executable `let` binding here: a top-level binding with
/// zero test coverage would drop this project below the `test:coverage`
/// target's 90%-line threshold before any real code exists to test. A type
/// alias (like `Domain.Types`'s pure DU/record declarations) has no
/// coverable sequence point, so the placeholder stays honest without
/// artificially depressing the baseline the threshold measures against.
module RhinoCli.Infrastructure.Placeholder

/// No infrastructure port exists yet — Wave A is the first to need one.
type NotYetPorted = NotYetPorted
