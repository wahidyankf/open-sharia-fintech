namespace OseBe.Contexts.Health

/// Infrastructure layer for the health bounded context.
///
/// The health context is stateless and has no infrastructure adapters (no
/// database, no external service). This module exists to anchor the layer in
/// the hexagonal slice.
module Infrastructure =

    /// Marker indicating the health context has no infrastructure dependencies.
    ///
    /// A niladic function rather than a plain module value: a top-level `let`
    /// binding of a trivial constant compiles to a `StartupCode` static
    /// initializer whose sequence point coverlet cannot attribute a runtime
    /// hit to (module-level value bindings are effectively constant-folded at
    /// call sites), leaving it permanently unreachable for line-coverage
    /// purposes regardless of how many tests call it. A function call is a
    /// real, instrumentable call site.
    let hasInfrastructureDependencies () : bool = false
