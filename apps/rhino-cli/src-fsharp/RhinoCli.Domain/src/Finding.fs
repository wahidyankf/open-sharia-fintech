/// Shared helpers over `RhinoCli.Domain.Types.Finding` used by more than one
/// caller. Folded out of `Md.fs`'s own private `hasBlockingFinding` copy
/// (Wave D PR11) once a second caller — the git pre-commit hook shim's
/// integration tests, composing `md links validate` and `md
/// heading-hierarchy validate`'s exit-code decision the same way
/// `Md.fs::findingsOutcome` already does for `md audit` — needed the
/// identical blocking-severity predicate and a shared plain-text rendering
/// [Repo-grounded — every Rust `md` command's `!findings.is_empty()` exit-code
/// check, e.g. `md_validate_heading_hierarchy.rs::run`].
module RhinoCli.Domain.Finding

open RhinoCli.Domain.Types

/// `true` when `findings` contains at least one `Blocking`-severity entry —
/// the standard pass/fail predicate every `Finding`-returning validator's
/// caller uses to decide its exit code.
let hasBlocking (findings: Finding list) : bool =
    findings |> List.exists (fun f -> f.Severity = Severity.Blocking)

/// Renders `findings` as human-readable text, one line per finding:
/// `path: message` when the finding is path-scoped, `message` alone
/// otherwise. Used by CLI-facing callers that have no bespoke formatter of
/// their own (unlike `md validate-mermaid`'s dedicated `formatMermaidText`,
/// which renders its own richer `MermaidValidationResult` shape).
let formatText (findings: Finding list) : string =
    findings
    |> List.map (fun f ->
        match f.Path with
        | Some path -> sprintf "%s: %s" path f.Message
        | None -> f.Message)
    |> String.concat "\n"
