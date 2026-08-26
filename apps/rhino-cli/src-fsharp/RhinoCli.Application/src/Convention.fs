/// Port of the Rust `convention` namespace's emoji, license, and aggregate
/// audit validators — see `apps/rhino-cli/src/application/repo_governance/
/// emoji_audit.rs`, `.../license_audit.rs`, and `apps/rhino-cli/src/commands/
/// convention_audit.rs`.
///
/// Wave A seeds this module scenario by scenario; see
/// `plans/in-progress/rewrite-rhino-cli-to-fsharp/delivery.md` Phase 3 for the
/// TDD cycle this module is built against. Findings are computed directly
/// against the real filesystem — no `Fs` port abstraction is introduced in
/// this wave since every consumer here is a real, on-disk scan.
module RhinoCli.Application.Convention

/// Runs the emoji validator over `paths` and returns `(exitCode, text)`,
/// mirroring `convention_validate_emoji::run`'s text-format output contract.
///
/// Not yet implemented — this cycle's `Convention` module carries no real
/// emoji-scanning logic yet, so every call reports a failure regardless of
/// input; a later cycle in this wave replaces this with the real scan.
let runEmojiValidate (_paths: string list) : int * string = 1, "EMOJI AUDIT: not yet implemented\n"

/// Returns the sorted `apps/<name>` and `libs/<name>` relative directory
/// paths under `repoRoot` that are expected to carry a `LICENSE` file.
///
/// Only the missing-file case is checked so far — SPDX cross-checking
/// against `LICENSING-NOTICE.md` is a later cycle's addition, so this does
/// not yet mirror `required_license_dirs`'s exemption/`-e2e` filtering.
let private requiredLicenseDirRelativePaths (repoRoot: string) : string list =
    [ "apps"; "libs" ]
    |> List.collect (fun parent ->
        let parentPath = System.IO.Path.Combine(repoRoot, parent)

        if System.IO.Directory.Exists parentPath then
            System.IO.Directory.EnumerateDirectories parentPath
            |> Seq.map (fun dir -> sprintf "%s/%s" parent (System.IO.Path.GetFileName dir))
            |> List.ofSeq
        else
            [])
    |> List.sort

/// Runs the license validator over `repoRoot` and returns `(exitCode, text)`,
/// mirroring `convention_validate_license::run`'s text-format output
/// contract.
///
/// Only detects a missing `LICENSE` file under `apps/` or `libs/` so far —
/// SPDX cross-checking against `LICENSING-NOTICE.md` is a later cycle's
/// addition.
let runLicenseValidate (repoRoot: string) : int * string =
    let missing =
        requiredLicenseDirRelativePaths repoRoot
        |> List.filter (fun rel -> not (System.IO.File.Exists(System.IO.Path.Combine(repoRoot, rel, "LICENSE"))))

    if List.isEmpty missing then
        0, "LICENSE AUDIT PASSED: no findings\n"
    else
        let body =
            missing
            |> List.map (fun rel -> sprintf "  [missing-license] %s — required directory has no LICENSE file\n" rel)
            |> String.concat ""

        1, sprintf "LICENSE AUDIT FAILED: %d finding(s)\n%s" missing.Length body

/// The convention validators run by `convention audit`, matching Rust's
/// `MEMBERS` constant in `convention_audit.rs`.
let private members = [ "emoji"; "license" ]

/// Runs every member validator in `MEMBERS` not present in `skip` against
/// `repoRoot`, aggregating pass/fail into one `(exitCode, text)` result,
/// mirroring `convention_audit::run`.
let runConventionAudit (repoRoot: string) (skip: string list) : int * string =
    let failures =
        members
        |> List.filter (fun name -> not (List.contains name skip))
        |> List.choose (fun name ->
            let code, _text =
                match name with
                | "emoji" -> runEmojiValidate [ repoRoot ]
                | "license" -> runLicenseValidate repoRoot
                | other -> 1, sprintf "unknown convention validator: %s" other

            if code = 0 then None else Some name)

    if List.isEmpty failures then
        let passedCount = members.Length - skip.Length
        0, sprintf "CONVENTION AUDIT PASSED: all %d validators passed\n" passedCount
    else
        let body =
            failures
            |> List.map (sprintf "  %s: validator reported failures\n")
            |> String.concat ""

        1, sprintf "CONVENTION AUDIT FAILED: %d validator(s) reported failures\n%s" failures.Length body
