/// Domain-level discriminated unions shared across every rhino-cli namespace
/// once it is ported from Rust. Filled wave by wave; Phase 2 seeds the three
/// types every namespace's finding/report shape already needs so later waves
/// extend rather than invent them: severity, a single finding, and the
/// supported CLI output format.
module RhinoCli.Domain.Types

/// The two-level severity scale every rhino-cli validator already uses
/// [Repo-grounded — `apps/rhino-cli/src/application/severity.rs`]: a
/// `Blocking` finding fails the pipeline (non-zero exit), an `Advisory` one
/// does not. Named `Blocking`/`Advisory` rather than the Rust source's literal
/// `Error`/`Warn` because a case literally named `Error` collides with
/// `FSharp.Core`'s own `Result.Error` — GRA-UNIONCASE-001 (treated as an
/// error in this project's lint target) catches that class of clash, and
/// `RequireQualifiedAccess` alone does not silence it.
[<RequireQualifiedAccess>]
type Severity =
    | Blocking
    | Advisory

/// One reported problem: its severity, a human-readable message, and the
/// repository-relative path it concerns, when the finding is path-scoped.
type Finding =
    { Severity: Severity
      Message: string
      Path: string option }

/// The `-o`/`--output` formats rhino-cli's Rust CLI already supports, per
/// `apps/rhino-cli/src/cli.rs`'s `OUTPUT` option.
type OutputFormat =
    | Text
    | Json
    | Markdown
