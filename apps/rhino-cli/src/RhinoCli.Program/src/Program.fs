/// Entry point and exit-code mapping for the F# `rhino-cli` port.
///
/// Wave A routes `convention` and `parity` into `RhinoCli.Cli.Dispatch`;
/// every other namespace name still falls through to its unrecognized-route
/// branch until its own wave replaces that fallthrough with a real case
/// [Repo-grounded — `apps/rhino-cli/src/main.rs`].
module RhinoCli.Program.Program

/// Rust's `anyhow`-based CLI maps an application error to exit code 1 and a
/// clean run to 0 [Repo-grounded — `apps/rhino-cli/src/main.rs`]. This F#
/// entry point preserves that same two-value contract; `RhinoCli.Cli.Dispatch`
/// widens it to `2` only for an argv shape no routed namespace recognizes.
[<EntryPoint>]
let main (argv: string[]) : int =
    match argv with
    | [||] -> 0
    | _ -> RhinoCli.Cli.Dispatch.route RhinoCli.Infrastructure.GitRoot.findRoot argv
