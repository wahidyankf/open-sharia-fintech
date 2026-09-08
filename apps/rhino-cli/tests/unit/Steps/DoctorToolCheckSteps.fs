/// Pure, in-process bindings for the Doctor behaviour. All resource inputs
/// are represented as values and both command ports are injected.
module RhinoCli.Tests.Unit.Steps.DoctorToolCheckSteps

open System
open System.Text.Json
open TickSpec
open Xunit
open RhinoCli.Application.Doctor

let private behaviourFeatureOwnership =
    [ "specs/apps/rhino/cli/behaviours/system/doctor.feature" ]

let private installedOutput name =
    match name with
    | "git" -> "git version 2.43.0"
    | "node" -> "v24.11.1"
    | "npm" -> "11.0.0"
    | "rust" -> "rustc 1.90.0"
    | "tofu" -> "OpenTofu v1.12.3"
    | name -> name + " 1.0.0"

let private parser name =
    match name with
    | "git" -> parseGitVersion
    | "rust" -> parseRustVersion
    | "tofu" -> parseTofuVersion
    | _ -> parseTrimVersion

let private syntheticInstall name _ _ =
    [ { Description = "Install " + name
        Command = "installer"
        Args = [ name ] } ]

let private def name required =
    { Name = name
      Binary = name
      Source = "in-memory requirement"
      Args = [ "--version" ]
      UseStderr = false
      ParseVer = parser name
      Compare = (if name = "tofu" then compareGte else compareExact)
      ReadReq = fun () -> required
      InstallCmd = Some(if name = "tofu" then installTofu else syntheticInstall name) }

/// The in-memory stand-in for the resolved Doctor inventory: the built-ins
/// plus whatever a scenario declared, exactly as `doctor.extra-tools` extends
/// the compiled-in list. `extra` is threaded per call rather than held in
/// module state so one scenario's declaration cannot leak into the next.
let private inventoryNames (extra: string list) = builtinDoctorToolInventory @ extra

let private inventory (extra: string list) =
    inventoryNames extra
    |> List.map (fun name ->
        let required =
            match name with
            | "node" -> "24.11.1"
            | "npm" -> "11.0.0"
            | "rust" -> "1.90.0"
            | "tofu" -> "1.12.3"
            | _ -> ""

        def name required)

type DoctorUnitWorld() =
    let mutable scope = FullScope
    let mutable selected: string list option = None
    let mutable skipped: string list = []
    let mutable extraTools: string list = []
    let mutable missing: Set<string> = Set.empty
    let mutable mismatchedNode = false
    let mutable rustBody: string option = None
    let mutable fixFlag = false
    let mutable dryRun = false
    let mutable json = false
    let mutable probed: string list = []
    let mutable output = ""
    let mutable error: string option = None
    let mutable succeeded = false

    let runner: CommandRunner =
        fun name _ ->
            probed <- name :: probed

            if Set.contains name missing then
                Error("not found: " + name)
            else
                Ok(installedOutput name, "", 0)

    let execute () =
        match
            selected
            |> Option.defaultValue []
            |> List.tryPick (
                parseDoctorToolName (inventoryNames extraTools)
                >> function
                    | Error e -> Some e
                    | Ok _ -> None
            )
        with
        | Some message ->
            error <- Some message
            succeeded <- false
        | None ->
            let defs =
                inventory extraTools
                |> List.map (fun d ->
                    if mismatchedNode && d.Name = "node" then
                        { d with ReadReq = fun () -> "1.0.0" }
                    else
                        d)
                |> fun defs -> selectToolDefs defs scope selected skipped

            let lintChecks =
                match rustBody with
                | Some body when defs |> List.exists (fun d -> d.Name = "rust") ->
                    rustToolchainLintComponentCheck "apps/rhino-cli/rust-toolchain.toml" body
                    |> Option.toList
                | _ -> []

            let result =
                (defs |> List.map (runOneDef runner)) @ lintChecks
                |> aggregateDoctorChecks scope

            let report =
                if json then
                    formatDoctorJsonAt (DateTimeOffset(2026, 9, 5, 0, 0, 0, TimeSpan.Zero)) result 7L
                else
                    formatDoctorText result false

            let progress = Text.StringBuilder()

            let fixResult =
                if fixFlag && hasRemediationWork result then
                    Some(
                        fixAtPlatform
                            "darwin"
                            result
                            defs
                            { DryRun = dryRun
                              Runner = Some(fun _ _ -> Ok()) }
                            (fun text -> progress.Append(text) |> ignore)
                    )
                else
                    None

            output <-
                report
                + progress.ToString()
                + (fixResult |> Option.map formatFixSummary |> Option.defaultValue "")
                + (if fixFlag && not (hasRemediationWork result) then
                       formatNothingToFix
                   else
                       "")

            succeeded <- result.MissingCount = 0
            error <- None

    member _.Output = output
    member _.Error = error
    member _.Probed = List.rev probed

    [<Given>]
    member _.``all required development tools are present with matching versions``() =
        missing <- Set.empty
        mismatchedNode <- false
        skipped <- []

    [<Given>]
    member _.``a required development tool is not found in the system PATH``() = missing <- Set.add "shellcheck" missing

    [<Given>]
    member _.``the tofu tool is not found in the system PATH``() = missing <- Set.add "tofu" missing

    [<Given>]
    member _.``the unselected shellcheck tool is not found in the system PATH``() =
        missing <- Set.add "shellcheck" missing

    [<Given>]
    member _.``only the tofu tool is selected``() = selected <- Some [ "tofu" ]

    [<Given>]
    member _.``an unknown Doctor tool is selected``() =
        selected <- Some [ "not-a-doctor-tool" ]

    [<Given>]
    member _.``a required development tool is installed with a non-matching version``() = mismatchedNode <- true

    [<Given>]
    member _.``a tool is listed under the doctor skip-tools section of repo-config.yml``() =
        skipped <- [ "shfmt" ]
        missing <- Set.add "shfmt" missing

    [<Given>]
    member _.``a tool is listed under the doctor extra-tools section of repo-config.yml``() = extraTools <- [ "java" ]

    [<Given>]
    member _.``a rust-toolchain.toml pins a channel and declares no lint components``() =
        rustBody <- Some "[toolchain]\nchannel = \"1.90.0\"\n"

    [<Given>]
    member _.``a rust-toolchain.toml declares only the clippy lint component``() =
        rustBody <- Some "[toolchain]\nchannel = \"1.90.0\"\ncomponents = [\"clippy\"]\n"

    [<When>]
    member _.``the developer runs the doctor command``() = execute ()

    [<When>]
    member _.``the developer runs the doctor command with JSON output``() =
        json <- true
        execute ()

    [<When>]
    member _.``the developer runs the doctor command with minimal scope``() =
        scope <- MinimalScope
        execute ()

    [<When>]
    member _.``the developer runs the doctor command with the fix flag``() =
        fixFlag <- true
        execute ()

    [<When>]
    member _.``the developer runs the doctor command with fix and dry-run flags``() =
        fixFlag <- true
        dryRun <- true
        execute ()

    [<When>]
    member _.``"npm run doctor" runs``() = execute ()

    [<Then>]
    member _.``the command exits successfully``() = Assert.True(succeeded, output)

    [<Then>]
    member _.``the command exits with a failure code``() = Assert.False(succeeded, output)

    [<Then>]
    member _.``the output reports each tool as passing``() = Assert.DoesNotContain("\u2717", output)

    [<Then>]
    member _.``the output identifies the missing tool``() = Assert.Contains("shellcheck", output)

    [<Then>]
    member _.``the output reports the tool as a warning rather than a failure``() =
        Assert.Contains("\u26A0", output)
        Assert.DoesNotContain("\u2717 node", output)

    [<Then>]
    member _.``the output is valid JSON``() =
        use _document = JsonDocument.Parse(output) in ()

    [<Then>]
    member _.``the JSON lists every checked tool with its status``() =
        use document = JsonDocument.Parse(output)
        Assert.Equal(16, document.RootElement.GetProperty("tools").GetArrayLength())

    [<Then>]
    member _.``the output checks only the minimal tool set``() =
        Assert.Contains("Summary: 6/6 tools OK", output)
        Assert.DoesNotContain(" rust ", output)

    [<Then>]
    member this.``the output reports only the selected tofu tool``() =
        Assert.Equal<string list>([ "tofu" ], this.Probed)
        Assert.Contains("Summary: 1/1 tools OK", output)

    [<Then>]
    member _.``the selected tofu dry run previews only its remediation``() =
        Assert.Contains("Would install: tofu", output)
        Assert.DoesNotContain("Would install: shellcheck", output)

    [<Then>]
    member _.``the invalid selection is rejected before any tool is probed``() =
        Assert.Empty(probed)
        Assert.Contains("unknown Doctor tool", error |> Option.defaultValue "")

    [<Then>]
    member _.``the output contains fix progress``() =
        Assert.Contains("Installing shellcheck", output)

    [<Then>]
    member _.``the output contains a dry-run preview``() =
        Assert.Contains("Would install: shellcheck", output)

    [<Then>]
    member _.``the output handles verified OpenTofu remediation safely``() =
        Assert.Contains("expected_checksum=", output)
        Assert.Contains("checksum mismatch", output)
        Assert.DoesNotContain("install-opentofu.sh", output)

    [<Then>]
    member _.``the output reports nothing to fix``() =
        Assert.Contains("Nothing to fix", output)

    [<Then>]
    member _.``the output does not include the skipped tool``() =
        Assert.DoesNotContain("shfmt", output)
        Assert.DoesNotContain("shfmt", String.concat " " probed)

    [<Then>]
    member this.``the output includes the configured extra tool``() =
        Assert.Contains("java", output)
        Assert.Contains("java", String.concat " " this.Probed)

    [<Then>]
    member _.``it reports the toolchain component check as a warning naming rustfmt and clippy``() =
        Assert.Contains("does not declare the rustfmt, clippy component", output)

    [<Then>]
    member _.``it reports the toolchain component check as a warning naming only rustfmt``() =
        Assert.Contains("does not declare the rustfmt component", output)
        Assert.DoesNotContain("rustfmt, clippy", output)
