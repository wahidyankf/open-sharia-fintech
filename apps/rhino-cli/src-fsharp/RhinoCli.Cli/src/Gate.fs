/// Renders `gate list` for one declared surface, in the exact text and JSON
/// shapes the Rust CLI layer emits
/// [Repo-grounded — `apps/rhino-cli/src/commands/gate/list.rs`].
///
/// Kept in `RhinoCli.Cli` rather than `RhinoCli.Application` because the Rust
/// source draws the same line: the registry itself is application state
/// (`repo_config`), while this per-surface projection and its two output
/// envelopes are a CLI-output concern.
module RhinoCli.Cli.Gate

open System
open System.IO
open System.Text.Json
open System.Text.Json.Nodes
open System.Text.Json.Serialization
open System.Text.Encodings.Web
open RhinoCli.Domain.Types
open RhinoCli.Application.RepoConfig

let private jsonOptions =
    let opts = JsonSerializerOptions()
    opts.WriteIndented <- true
    opts.Encoder <- JavaScriptEncoder.UnsafeRelaxedJsonEscaping
    opts.DefaultIgnoreCondition <- JsonIgnoreCondition.WhenWritingNull
    opts

/// JSON-friendly projection of one gate on one surface, mirroring Rust's
/// `GateListEntry`. `hand_wired` is deliberately absent: Rust marks it
/// `#[serde(skip_serializing)]` and uses it only to pick the text-format
/// marker.
type GateListEntryJson =
    { id: string
      [<JsonPropertyName("type")>]
      gateType: string
      command: string
      doctor_tools: string list
      scope: string
      [<JsonPropertyName("carve-out")>]
      carveOut: string
      category: string
      verifies: string
      wiring: string
      surfaces: string list }

/// JSON-friendly projection of one declared `ci_group` and its members,
/// mirroring Rust's `GateGroupEntry`.
type GateGroupEntryJson =
    { group: string
      gates: string list
      doctor_tools: string list }

/// serde omits an absent optional string; System.Text.Json omits `null`.
let private orNull (value: string option) : string =
    match value with
    | Some text -> text
    | None -> null

let private surfaceName (surface: GateSurface) : string =
    match surface with
    | CommitMsg -> "commit-msg"
    | PreCommit -> "pre-commit"
    | PrePush -> "pre-push"
    | Ci -> "ci"

let private gateTypeName (gateType: GateType) : string =
    match gateType with
    | Check -> "check"
    | Mutation -> "mutation"

let private scopeName (scope: ScopeKind) : string =
    match scope with
    | AffectedFileType -> "affected-file-type"
    | AllFileType -> "all-file-type"
    | AffectedProjects -> "affected-projects"
    | AllProjects -> "all-projects"
    | Other -> "other"
    | PathGated -> "path-gated"

let private carveOutName (carveOut: GateCarveOut option) : string option =
    carveOut |> Option.map (fun StagedOnly -> "staged-only")

let private wiringName (wiring: GateWiring option) : string option =
    wiring
    |> Option.map (fun value ->
        match value with
        | Matrix -> "matrix"
        | HandWired -> "hand-wired")

/// Parses a command-line surface name into its registry variant
/// [Repo-grounded — `gate/list.rs::parse_surface`].
let parseSurface (surface: string) : Result<GateSurface, string> =
    match surface with
    | "commit-msg" -> Ok CommitMsg
    | "pre-commit" -> Ok PreCommit
    | "pre-push" -> Ok PrePush
    | "ci" -> Ok Ci
    | other -> Error(sprintf "unknown gate surface \"%s\": expected one of commit-msg, pre-commit, pre-push, ci" other)

/// Rejects a duplicate gate id on one surface, or an `--only` selector that
/// does not select exactly one gate
/// [Repo-grounded — `gate/list.rs::validate_gate_ids`].
let validateGateIds (gates: GateEntry list) (only: string option) : Result<unit, string> =
    match only with
    | Some id ->
        let count = gates |> List.filter (fun gate -> gate.Id = id) |> List.length

        if count <> 1 then
            Error(sprintf "--only gate id \"%s\" must select exactly one gate, found %d" id count)
        else
            Ok()
    | None ->
        let duplicate =
            gates
            |> List.mapi (fun index gate -> index, gate)
            |> List.tryFind (fun (index, gate) ->
                gates |> List.take index |> List.exists (fun other -> other.Id = gate.Id))

        match duplicate with
        | Some(_, gate) -> Error(sprintf "duplicate gate id \"%s\"" gate.Id)
        | None -> Ok()

/// Returns the gates whose declared `ci_group` equals `groupId`, preserving
/// registry declaration order
/// [Repo-grounded — `gate/list.rs::gates_in_ci_group`].
let gatesInCiGroup (gates: GateEntry list) (groupId: string) : GateEntry list =
    gates |> List.filter (fun gate -> gate.CiGroup = Some groupId)

/// Groups gates by their declared `ci_group`, preserving each group's
/// first-appearance order and each gate's registry declaration order within
/// the group [Repo-grounded — `gate/list.rs::group_by_ci_group`].
let private groupByCiGroup (gates: GateEntry list) : Result<(string * GateEntry list) list, string> =
    let missing = gates |> List.tryFind (fun gate -> gate.CiGroup.IsNone)

    match missing with
    | Some gate -> Error(sprintf "gate \"%s\" is missing ci_group required for grouped output" gate.Id)
    | None ->
        let groupIds =
            gates
            |> List.choose (fun gate -> gate.CiGroup)
            |> List.fold (fun acc id -> if List.contains id acc then acc else acc @ [ id ]) []

        Ok(groupIds |> List.map (fun groupId -> groupId, gatesInCiGroup gates groupId))

/// Returns the deduped, sorted union of every gate's declared `doctor_tools`
/// [Repo-grounded — `gate/list.rs::union_doctor_tools`].
let private unionDoctorTools (gates: GateEntry list) : string list =
    gates
    |> List.collect (fun gate -> gate.DoctorTools)
    |> List.distinct
    |> List.sort

let private writeGrouped (gates: GateEntry list) (outputFormat: OutputFormat) : Result<string, string> =
    match groupByCiGroup gates with
    | Error message -> Error message
    | Ok groups ->
        match outputFormat with
        | OutputFormat.Json ->
            let entries =
                groups
                |> List.map (fun (group, members) ->
                    { group = group
                      doctor_tools = unionDoctorTools members
                      gates = members |> List.map (fun gate -> gate.Id) })

            Ok(JsonSerializer.Serialize(entries, jsonOptions) + "\n")
        | OutputFormat.Text
        | OutputFormat.Markdown ->
            groups
            |> List.map (fun (group, members) ->
                let ids = members |> List.map (fun gate -> gate.Id) |> String.concat ", "
                sprintf "%s\t%s\n" group ids)
            |> String.concat ""
            |> Ok

/// Lists gates declared on one surface at a known repository root
/// [Repo-grounded — `gate/list.rs::run_at_root`].
let listAtRoot
    (repoRoot: string)
    (surface: string)
    (outputFormat: OutputFormat)
    (byGroup: bool)
    : Result<string, string> =
    match parseSurface surface with
    | Error message -> Error message
    | Ok surface ->
        match load repoRoot with
        | Error message -> Error message
        | Ok config ->
            let surfaceGates =
                config.Gates
                |> List.filter (fun gate -> gate.Surfaces |> List.exists (fun (declared, _) -> declared = surface))

            match validateGateIds surfaceGates None with
            | Error message -> Error message
            | Ok() ->
                if byGroup then
                    // Hand-wired gates are excluded from every grouped output
                    // format, matching `gate run --group`'s unconditional
                    // filter: they are dispatched by their own dedicated CI
                    // workflow job rather than by `--group`.
                    surfaceGates
                    |> List.filter (fun gate -> gate.Wiring <> Some HandWired)
                    |> fun gates -> writeGrouped gates outputFormat
                else
                    let visibleGates =
                        surfaceGates
                        |> List.filter (fun gate -> outputFormat <> OutputFormat.Json || gate.Wiring <> Some HandWired)

                    let scopeOf (gate: GateEntry) =
                        gate.Surfaces
                        |> List.pick (fun (declared, scope) -> if declared = surface then Some scope else None)

                    match outputFormat with
                    | OutputFormat.Json ->
                        let entries =
                            visibleGates
                            |> List.map (fun gate ->
                                { id = gate.Id
                                  gateType = gateTypeName gate.GateType
                                  command = gate.Command
                                  doctor_tools = gate.DoctorTools
                                  scope = scopeName (scopeOf gate).Scope
                                  carveOut = orNull (carveOutName gate.CarveOut)
                                  category = orNull gate.Category
                                  verifies = orNull gate.Verifies
                                  wiring = orNull (wiringName gate.Wiring)
                                  surfaces = gate.Surfaces |> List.map (fst >> surfaceName) })

                        Ok(JsonSerializer.Serialize(entries, jsonOptions) + "\n")
                    | OutputFormat.Text
                    | OutputFormat.Markdown ->
                        visibleGates
                        |> List.map (fun gate ->
                            let marker = if gate.Wiring = Some HandWired then "\thand-wired" else ""

                            let carveOut =
                                match carveOutName gate.CarveOut with
                                | Some value -> sprintf "\tcarve-out=%s" value
                                | None -> ""

                            sprintf
                                "%s\t%s\t%s\t%s%s%s\n"
                                gate.Id
                                (gateTypeName gate.GateType)
                                gate.Command
                                (scopeName (scopeOf gate).Scope)
                                marker
                                carveOut)
                        |> String.concat ""
                        |> Ok

/// The lightweight resolver shim generated `rhino-cli`-kind commands invoke
/// instead of a `cargo run` invocation, whose invocation-check tax every
/// hook/gate call would otherwise pay
/// [Repo-grounded — `gate/emit.rs::RHINO_CLI_RESOLVER_SHIM`].
let rhinoCliResolverShim = "apps/rhino-cli/scripts/rhino-bin.sh"

/// Splits a command string into its leading whitespace-delimited token and
/// the whitespace-trimmed remainder
/// [Repo-grounded — `gate/emit.rs::split_leading_token`].
let private splitLeadingToken (command: string) : string * string =
    match command |> Seq.tryFindIndex Char.IsWhiteSpace with
    | None -> command, ""
    | Some index -> command.Substring(0, index), command.Substring(index + 1).TrimStart()

/// Rewrites a node-resolved gate's command to invoke its tool through the
/// repository-local `node_modules/.bin` directory instead of `npx`, whose own
/// resolution/download check runs even when the package is installed
/// [Repo-grounded — `gate/emit.rs::node_modules_bin_command`].
let private nodeModulesBinCommand (command: string) : string =
    let rec skipNpxFlags (arguments: string) : string * string =
        let nextTool, nextArguments = splitLeadingToken arguments

        if nextTool.StartsWith("-", StringComparison.Ordinal) then
            skipNpxFlags nextArguments
        else
            nextTool, nextArguments

    let leadingTool, leadingArguments = splitLeadingToken command

    let tool, arguments =
        if leadingTool = "npx" then
            skipNpxFlags leadingArguments
        else
            leadingTool, leadingArguments

    if arguments = "" then
        sprintf "node_modules/.bin/%s" tool
    else
        sprintf "node_modules/.bin/%s %s" tool arguments

/// Whether a `kind: external` gate resolves its tool from this repository's
/// `node_modules` rather than a system `PATH` binary, signalled by the
/// registry's existing `doctor-tools: [npm]` declaration
/// [Repo-grounded — `gate/emit.rs::is_node_resolved`].
let private isNodeResolved (gate: GateEntry) : bool = gate.DoctorTools |> List.contains "npm"

/// Quotes one generated argument for lint-staged's POSIX-shell command
/// string, keeping configuration values literal
/// [Repo-grounded — `gate/emit.rs::shell_quote`].
let private shellQuote (argument: string) : string =
    let escaped =
        argument.Replace("\\", "\\\\").Replace("\"", "\\\"").Replace("$", "\\$").Replace("`", "\\`")

    sprintf "\"%s\"" escaped

/// Quotes a whole script for `bash -c`, retaining literal shell expansion
/// inside it [Repo-grounded — `gate/emit.rs::shell_script_quote`].
let private shellScriptQuote (script: string) : string =
    sprintf "'%s'" (script.Replace("'", "'\"'\"'"))

/// Renders a registry command with its fixed arguments for a generated shell
/// command [Repo-grounded — `gate/emit.rs::command_with_fixed_arguments`].
let private commandWithFixedArguments (gate: GateEntry) : string =
    let command =
        match gate.Kind with
        | RhinoCli -> sprintf "%s %s" rhinoCliResolverShim gate.Command
        | External when isNodeResolved gate -> nodeModulesBinCommand gate.Command
        | External
        | Nx -> gate.Command

    match fixedArguments gate with
    | [] -> command
    | arguments ->
        let quoted =
            arguments
            |> List.mapi (fun index argument -> if index % 2 = 0 then argument else shellQuote argument)
            |> String.concat " "

        sprintf "%s %s" command quoted

/// Whether a pre-commit file-scoped gate belongs in lint-staged's one batch:
/// formatter mutations run inside it so their output reaches later
/// validators, while other mutations stay direct hook work
/// [Repo-grounded — `gate/emit.rs::is_lint_staged_eligible`].
let private isLintStagedEligible (gate: GateEntry) : bool =
    gate.GateType = Check
    || (gate.GateType = Mutation && gate.Category = Some "formatter")

/// Renders one gate as the command lint-staged must execute for its glob
/// [Repo-grounded — `gate/emit.rs::lint_staged_command`].
let private lintStagedCommand (gate: GateEntry) (scope: SurfaceScope) : string =
    let command = commandWithFixedArguments gate

    match scope.LintStagedShell with
    | None -> command
    | Some template ->
        let body =
            match template.IndexOf("{{command}}", StringComparison.Ordinal) with
            | -1 -> template
            | at ->
                template.Substring(0, at)
                + command
                + template.Substring(at + "{{command}}".Length)

        sprintf "bash -c %s --" (shellScriptQuote body)

/// Derives the `lint-staged` block from pre-commit affected-file gates,
/// keeping each glob's first-occurrence order rather than sorting: that order
/// is the generated artifact's declaration-order contract
/// [Repo-grounded — `gate/emit.rs::lint_staged_from_config`].
let lintStagedFromConfig (config: RepoConfig) : (string * string list) list =
    let addCommand (acc: (string * string list) list) (glob: string) (command: string) =
        if acc |> List.exists (fun (declared, _) -> declared = glob) then
            acc
            |> List.map (fun (declared, commands) ->
                if declared = glob then
                    declared, commands @ [ command ]
                else
                    declared, commands)
        else
            acc @ [ glob, [ command ] ]

    config.Gates
    |> List.fold
        (fun acc gate ->
            let preCommit =
                gate.Surfaces
                |> List.tryPick (fun (surface, scope) -> if surface = PreCommit then Some scope else None)

            match preCommit with
            | Some scope when scope.Scope = AffectedFileType && isLintStagedEligible gate ->
                let command = lintStagedCommand gate scope

                Option.toList scope.Glob @ scope.Globs
                |> List.fold (fun acc glob -> addCommand acc glob command) acc
            | _ -> acc)
        []

/// Emits the configured gate surface into its generated artifact at a known
/// repository root [Repo-grounded — `gate/emit.rs::emit_at_root`].
let emitAtRoot (repoRoot: string) (surface: string) : Result<string, string> =
    if surface <> "pre-commit" then
        Error "gate emit currently supports only surface pre-commit"
    else
        match load repoRoot with
        | Error message -> Error message
        | Ok config ->
            let packagePath = Path.Combine(repoRoot, "package.json")

            try
                let node = JsonNode.Parse(File.ReadAllText packagePath)

                match node with
                | :? JsonObject as package ->
                    let block = JsonObject()

                    for glob, commands in lintStagedFromConfig config do
                        let array = JsonArray()

                        for command in commands do
                            array.Add(JsonValue.Create command)

                        block.Add(glob, array)

                    // Marker-first: replacing an existing key in place keeps
                    // its position, so re-emitting is byte-identical.
                    if package.ContainsKey "lint-staged" then
                        package.["lint-staged"] <- block
                    else
                        package.Add("lint-staged", block)

                    File.WriteAllText(packagePath, package.ToJsonString jsonOptions + "\n")
                    Ok "Emitted lint-staged from gate surface pre-commit\n"
                | _ -> Error "package.json must contain a JSON object"
            with ex ->
                Error(sprintf "cannot read %s: %s" packagePath ex.Message)
