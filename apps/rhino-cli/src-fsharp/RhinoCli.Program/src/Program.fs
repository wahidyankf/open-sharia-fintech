/// Entry point and exit-code mapping for the F# `rhino-cli` port.
///
/// Phase 2 seeds this module with no routed namespace — `FSHARP_NAMESPACES`
/// in `apps/rhino-cli/scripts/rhino-bin.sh` ships empty, so no wave's shim
/// flip reaches this binary yet. Each wave replaces the placeholder match
/// arm below with a real dispatch into `RhinoCli.Cli`'s parsed namespace.
module RhinoCli.Program.Program

/// Rust's `anyhow`-based CLI maps an application error to exit code 1 and a
/// clean run to 0 [Repo-grounded — `apps/rhino-cli/src/main.rs`]. This F#
/// entry point preserves that same two-value contract until a wave adds a
/// namespace that needs a wider one.
[<EntryPoint>]
let main (argv: string[]) : int =
    match argv with
    | [||] -> 0
    | _ ->
        eprintfn "rhino-cli-fsharp: no namespace is routed to F# yet (FSHARP_NAMESPACES is empty)"
        1
