/// One module per spec directory family, filled wave by wave, mirroring the
/// Rust `application/` module tree. Phase 2 seeds an empty module so the
/// project builds and references both lower layers before any namespace
/// ports real validators or reporters.
///
/// Deliberately no executable `let` binding here — see
/// `RhinoCli.Infrastructure.Placeholder`'s doc comment for why. The type
/// alias below still proves the `RhinoCli.Domain` project reference is live
/// (a stale/unused `ProjectReference` would fail to resolve `Finding` here)
/// without adding a coverable, currently-untested line.
module RhinoCli.Application.Placeholder

/// No validator is ported yet — Wave A is the first to need one.
type NotYetPortedFindings = RhinoCli.Domain.Types.Finding list
